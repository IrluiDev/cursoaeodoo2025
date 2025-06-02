from odoo import models, fields


class MusicSchoolLesson(models.Model):
    _name = 'music.school.lesson'
    _description = 'Lessons'
    _rec_name = 'course_id'


    teacher_id = fields.Many2one(
        comodel_name='music.school.teacher',
        string="Teacher",
        help="Teacher responsible for the lesson"
    )
    course_id = fields.Many2one(
        comodel_name='music.school.course',
        string="Course",
        help="Course associated with the lesson"
    )
    room_id = fields.Many2one(
        comodel_name='music.school.room',
        string="Room",
        help="Room where the lesson takes place"
    )
    date = fields.Datetime(
        string="Date",
        help="Date and time when the lesson takes place"
    )
    duration = fields.Float(
        string="Duration (hours)",
        help="Duration of the lesson in hours"
    )
    notes = fields.Text(
        string="Notes",
        help="Additional notes about the lesson"
    )

    color = fields.Integer(
        string="Color",
        help="Color associated with the lesson for calendar views"
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('done', 'Done'),
            ('postponed', 'Postponed'),
            ('cancelled', 'Cancelled'),
        ],
        string="State",
        default='draft',
        help="Current state of the lesson",
        group_expand='group_expand_state'
    )

    def group_expand_state(self, states, domain):
        return [key for key, val in type(self).state.selection]