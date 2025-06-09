from odoo import models, fields, Command, api


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

    day_duration = fields.Integer(
        string="Duration day",
        compute='_compute_day_duration',
        help="Duration of the course in days",
        store=True
    )

    student_ids = fields.Many2many(
        comodel_name='music.school.student',
        string="Students",
        help="Students enrolled in the course"
    )

    @api.depends('start_date', 'end_date')
    def _compute_day_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                start = fields.Date.from_string(record.start_date)
                end = fields.Date.from_string(record.end_date)
                record.day_duration = (end - start).days + 1
            else:
                record.day_duration = 0

    def action_draft(self):
        for record in self:
            record.state = 'draft'
    
    def action_progress(self):
        for record in self:
            record.state = 'progress'

    def action_finish(self):
        for record in self:
            record.state = 'finished'
            lessons = self.env['music.school.lesson'].search([('course_id','=', record.id)])
            #lessons.state = 'done'
            lessons.write({'state': 'done'})
    
    def group_expand_state(self, states, domain):
        return [key for key, val in type(self).state.selection]

    def create_lesson(self):
        vals = {
            'course_id': self.id,
            'teacher_id': self.teacher_id.id,
        }
        lesson = self.env['music.school.lesson'].create(vals)
    
    def assign_students(self):
        for record in self:
            students = self.env['music.school.student'].search([])
            if students:
                #record.student_ids = [(6, 0, students.ids)]
                #record.write({'student_ids': [(6, 0, students.ids)]})
                record.student_ids = students
                #record.student_ids = [Command.set(students.ids)]
                #record.write({
                #     'student_ids': [Command.set(student.ids)]
                # })