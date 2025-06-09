from odoo import models, fields


class MusicSchoolLessonAttendance(models.Model):
    _name = 'music.school.lesson.attendance'
    _description = 'Attendance for Music School Lessons'
    _rec_name = 'student_id'

    lesson_id = fields.Many2one(
        comodel_name='music.school.lesson',
        string="Lesson",
        help="Lesson for which the attendance is recorded",
    )

    student_id = fields.Many2one(
        comodel_name='music.school.student',
        string="Student",
    )
    is_present = fields.Boolean(
        string="Is Present",
    )

    date = fields.Datetime(
        string="Date",
        help="Date and time of the attendance record",)
    
    notes = fields.Text(
        string="Notes",
        help="Additional notes about the attendance record",
    )
    