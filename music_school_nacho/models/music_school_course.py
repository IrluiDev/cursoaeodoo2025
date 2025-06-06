from odoo import models, fields


class MusicSchoolCourse(models.Model):
    _name = 'music.school.course'
    _description = 'Courses'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('progress', 'In progress'),
            ('finished', 'Finished'),
        ],
        string="State",
        default='draft',
        group_expand='group_expand_state'
    )
    teacher_id = fields.Many2one(
        comodel_name='music.school.teacher',
        string="Teacher",
        help="Teacher responsible for the course"
    )

    instrument_id = fields.Many2one(
        comodel_name='music.school.instrument',
        string="Instrument",
        help="Instrument associated with the course"
    )
    level = fields.Selection(
        selection=[
            ('none', 'None'),
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        string="Level",
        default='beginner',
    )
    start_date = fields.Date(
        string="Start Date",
        help="Date when the course starts"
    )
    end_date = fields.Date(
        string="End Date",
        help="Date when the course ends"
    )

    capacity = fields.Integer(
        string="Capacity",
        help="Maximum number of students allowed in the course"
    )

    color = fields.Integer(
        string="Color",
        help="Color associated with the course for calendar views"
    )

    def action_draft(self):
        for record in self:
            record.state = 'draft'
    
    def action_progress(self):
        for record in self:
            record.state = 'progress'

    def action_finish(self):
        for record in self:
            record.state = 'finished'
    
    def group_expand_state(self, states, domain):
        return [key for key, val in type(self).state.selection]
