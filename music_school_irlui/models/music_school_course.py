from odoo import models, fields, Command, api
from odoo.exceptions import UserError
from datetime import timedelta, date

class MusicSchoolCourse(models.Model):
    _name = 'music.school.course'
    _description = 'Courses'

    name = fields.Char(string="Name", required=True, translate=True)
    description = fields.Text(string="Description")
    sequence = fields.Integer(string='Sequence', default=10)
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
        help="Teacher assigned to the course",
    )
    instrument_id = fields.Many2one(
        comodel_name='music.school.instrument',
        string="Instrument",
        help="Instrument associated with the course",
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
        help="Start date of the course",
    )
    end_date = fields.Date(
        string="End Date",
        help="End date of the course",
    )
    days_duration = fields.Integer(
        string="Duration (days)",
        help="Duration of the course in days",
        compute='_compute_days_duration',
        store=True,
    )
    days_remaining = fields.Integer(
        string="Days Remaining",
        help="Number of days remaining until the course ends",
        compute='_compute_days_remaining',
        store=True,
    )
    capacity = fields.Integer(
        string="Capacity",
        help="Maximum number of students allowed in the course",
    )
    color = fields.Integer(
        string="Color",
        help="Color of the course for calendar view",
    )
    student_ids = fields.Many2many(
        comodel_name='music.school.student',
        string="Students",
        help="Students enrolled in the course",
    )
    def action_draft(self):
        for record in self:
            record.state = 'draft'
    
    def action_progress(self):
        for record in self:
            record.state = 'progress'
    
    def action_finished(self):
        self.ensure_one()
        # Cambia el estado a finished (o haz más cosas)
        self.write({'state': 'finished'})
    
    def create_lesson(self):
        vals = {
            'course_id': self.id,
            'teacher_id': self.teacher_id.id,
        }
        lesson = self.env['music.school.lesson'].create(vals)
    
    def group_expand_state(self, states, domain):
        return [key for key, val in type(self).state.selection]

    def assign_students(self):
        for record in self:
            students = self.env['music.school.student'].search([])
            if students:
                record.student_ids = students
    
    def _compute_days_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                duration = (record.end_date - record.start_date).days
                record.days_duration = duration
            else:
                record.days_duration = 0

    @api.depends('end_date')
    def _compute_days_remaining(self):
        today = date.today()
        for record in self:
            if record.end_date and record.end_date > today:
                record.days_remaining = (record.end_date - today).days
            else:
                record.days_remaining = 0

