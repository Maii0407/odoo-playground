from odoo import fields, models
from datetime import timedelta

class Property(models.Model):
  _name = "estate.property"
  _description = "Estate Properties"

  name = fields.Char('Property Name', required=True, translate=True)
  description = fields.Text()
  postcode = fields.Char()
  date_availability = fields.Date('Property Availability Date', copy=False, default=lambda self: fields.Datetime.today() + timedelta(days=90))
  expected_price = fields.Float('Property Expected Price', required=True)
  selling_price = fields.Float('Property Selling Price', readonly=True, copy=False)
  bedrooms = fields.Integer('Property Number of Bedrooms', default=2)
  living_area = fields.Integer()
  facades = fields.Integer()
  garage = fields.Boolean()
  garden = fields.Boolean()
  garden_area = fields.Integer()
  garden_orientation = fields.Selection(
    string='Garden Orientation of Property',
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
