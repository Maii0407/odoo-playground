from odoo import fields, models
from datetime import timedelta

class Property(models.Model):
  _name = "estate.property"
  _description = "Estate Properties"

  name = fields.Char('Title', required=True, translate=True)
  description = fields.Text()
  postcode = fields.Char('Postcode')
  date_availability = fields.Date('Available From', copy=False, default=lambda self: fields.Datetime.today() + timedelta(days=90))
  expected_price = fields.Float('Expected Price', required=True)
  selling_price = fields.Float('Selling Price', readonly=True, copy=False)
  bedrooms = fields.Integer('Bedrooms', default=2)
  living_area = fields.Integer('Living Area (sqm)')
  facades = fields.Integer()
  garage = fields.Boolean()
  garden = fields.Boolean()
  garden_area = fields.Integer('Garden Area (sqm)')
  garden_orientation = fields.Selection(
    string='Garden Orientation',
    selection=[
      ('north', 'North'),
      ('south', 'South'),
      ('east', 'East'),
      ('west', 'West')
    ]
  )
  active = fields.Boolean(default=True)
  state = fields.Selection(
    string='Property State',
    required=True,
    default='new',
    selection=[
      ('new', 'New'),
      ('offer received', 'Offer Received'),
      ('offer accepted', 'Offer Accepted'),
      ('sold', 'Sold'),
      ('canceled', 'Canceled')
    ]
  )
  property_type_id = fields.Many2one("estate.property.type", string="Property Type")
  buyer = fields.Many2one("res.partner", string="Buyer", index=True, copy=False)
  salesperson = fields.Many2one("res.users", string="Salesman", index=True, default=lambda self:self.env.user)
  tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
  offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
