from ejudge.feedback import Feedback
from ejudge import graders
import ejudge.contrib.pytuga
from iospec import parse_string as parse_iospec
from django.db import models
from model_utils.managers import InheritanceManager
from picklefield import PickledObjectField
from wagtail.wagtailcore.fields import RichTextField
from codeschool.shortcuts import lazy, delegation
from codeschool import constants
from cs_courses import models as courses_models
from cs_activities.models import Activity, Feedback


#
# Base Question class
#
class Question(models.Model):
    """Base class for all question types"""

    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=140)
    long_description = RichTextField()
    author_name = models.CharField('Author', max_length=100, blank=True)
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    question_type = models.IntegerField(null=True)
    discipline = models.ForeignKey(courses_models.Discipline, blank=True, null=True)

    objects = InheritanceManager()

    class Meta:
        permissions = (("download_question", "Can download question files"),)

    def __str__(self):
        return self.title


#
# Basic question types: question_type starts at 10 up to 99
#
class FreeAnswerQuestion(Question):
    pass


class NumericQuestion(Question):
    answer_start = models.FloatField()
    answer_end = models.FloatField(blank=True, null=True)
    is_exact = models.BooleanField(default=True)


class BooleanQuestion(Question):
    answer_key = models.BooleanField()


class StringMatchQuestion(Question):
    template = models.TextField()
    is_regex = models.BooleanField(default=True)


#
# Programming related questions: question_types starts at 100 up to 999
#
class CodeIoQuestion(Question):
    """CodeIo questions evaluates code and judge them by their inputs and
    outputs."""

    response_computed_template = models.TextField(blank=True)
    response_template = models.TextField(
            'Response template',
            blank=True,
            help_text='Template used to grade I/O responses. See http://??? for'
                      'a complete reference on the template format.',
    )
    timeout = models.FloatField(
            'Timeout',
            default=1.0,
            help_text='Timeout in seconds',
    )
    grader = PickledObjectField(null=True)

    class Meta:
        verbose_name = 'I/O coding question'
        verbose_name_plural = 'I/O coding questions'

    @lazy
    def template(self):
        """Prepare the IOGroup template object for the current CodeIoQuestion.

        This method uses data in self.io_template and build the correct template
        by running it with all available answers. If some answer fails, or if
        different languages yield different results, a RuntimeError is raised.
        """

        template_src = self._compute_computed_template()
        return parse_iospec(template_src)

    def _compute_computed_template(self):
        if not self.response_computed_template:
            input_template = parse_iospec(self.response_template)
            template_final = None

            # See if all answer keys agree with each other
            for answer_key in self.answer_keys.all():
                src = answer_key.source_code
                lang = answer_key.language
                template = graders.run(src, input_template, lang=lang)
                if template_final is None:
                    template_final = template
                elif template_final != template:
                    raise ValueError('answer keys do not aggree')
            self.response_computed_template = template_final.source()
            self.save(update_fields=['response_computed_template'])

        return self.response_computed_template


class CodeIoAnswerKey(models.Model):
    """Represents an answer to some question given in some specific computer
    language plus the placeholder text that should be displayed"""

    prototype = models.ForeignKey(CodeIoQuestion, related_name='answer_keys')
    language = models.CharField(
            'Programming language',
            max_length=10,
            choices=constants.language_choices)
    source_code = models.TextField(
            'Answer source code',
            default='',
            help_text='Source code for the correct answer in the given '
                      'programming language',
    )
    placeholder = models.TextField(
            'Placeholder code',
            blank=True,
            help_text='This optional field controls which code should be '
                      'placed in the source code editor when a question is '
                      'opened. This is useful to put boilerplate or even a '
                      'full program that the student should modify. It is '
                      'possible to configure a global per-language boilerplate '
                      'and leave this field blank.',
    )
    response_template_extra = models.TextField(
            'Extra reponses',
            blank=True,
            help_text='Additional test cases specific for this language.',
    )
    response_computed_template = models.TextField(blank=True)
    grader_function = PickledObjectField()

    class Meta:
        verbose_name = 'Answer key'
        verbose_name_plural = 'Answer keys'

    @lazy
    def template(self):
        template_src = self._compute_computed_template()
        return parse_iospec(template_src)

    def _compute_computed_template(self):
        #TODO: fixme
        if self.response_computed_template:
            return self.response_computed_template
        elif not self.response_template_extra:
            return self.prototype._compute_computed_template()
        else:
            raise NotImplementedError

        extra = parse_iospec(self.response_template_extra)
        full_template = self.prototype.template
        full_template.extend(extra)
        self.response_computed_template = full_template.source()
        self.save(update_fields=['response_template'])
        return self.response_computed_template

    @property
    def question_type(self):
        return CodeIoQuestion._class_type

    def __str__(self):
        return self.language

    def grade(self, response):
        lang = self.language
        src = response.text
        iospec = self.template
        feedback = graders.io.grade(src, iospec, lang=lang)
        return CodeIoFeedback.from_feedback(feedback, response)


@delegation('question', ['long_description', 'short_description'])
class QuestionActivity(Activity):
    question = models.ForeignKey(Question)

    @property
    def name(self):
        return self.question.title


class CodeIoActivity(QuestionActivity):
    answer_key = models.ForeignKey(CodeIoAnswerKey)


class CodeIoFeedback(Feedback):
    case = models.TextField()
    answer_key = models.TextField()
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    hint = models.TextField(blank=True)
    message = models.TextField(blank=True)

    @classmethod
    def from_feedback(cls, feedback, response):
        case = feedback.case
        answer_key = feedback.answer_key

        return CodeIoFeedback(
            response=response,
            grade=feedback.grade,
            case=case.source(),
            answer_key=answer_key.source(),
            title=feedback.title(),
            status=feedback.status(),
            hint=feedback.hint,
            message=feedback.message,
        )

    @lazy
    def _feedback(self):
        case = parse_iospec(self.case)
        answer_key = parse_iospec(self.answer_key)
        return Feedback(case, answer_key, title=self.title, status=self.status,
                        hint=self.hint, message=self.message)

    def html(self):
        return self._feedback.html()