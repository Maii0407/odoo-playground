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
