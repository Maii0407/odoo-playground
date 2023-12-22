from odoo import api, fields, models, tools
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError

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
  total_area = fields.Integer('Total Area (sqm)', compute="_compute_total_area")
  best_price = fields.Float('Best Offer', compute="_compute_best_price")

  _sql_constraints = [
    (
      'check_expected_price',
      'CHECK(expected_price > 0)',
      'Property expected price must be positive value'
    ),
    (
      'check_selling_price',
      'CHECK(selling_price > 0)',
      'Property selling price must be positive value'
    )
  ]

  @api.depends("living_area", "garden_area")
  def _compute_total_area(self):
    for record in self:
      record.total_area = record.living_area + record.garden_area

  @api.depends("offer_ids.price")
  def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            if prices:
                record.best_price = max(prices)
            else:
                record.best_price = 0.0

  @api.onchange("garden")
  def _onchange_garden(self):
    if self.garden:
      self.garden_area = 10
      self.garden_orientation = 'north'
    else:
      self.garden_area = 0
      self.garden_orientation = ''

  @api.constrains("selling_price", "expected_price")
  def _check_selling_price(self):
      for record in self:
          if not tools.float_is_zero(record.selling_price, precision_digits=2) and not tools.float_is_zero(record.expected_price, precision_digits=2):
              min_selling_price = 0.9 * record.expected_price
              if tools.float_compare(record.selling_price, min_selling_price, precision_digits=2) == -1:
                  raise ValidationError("Selling Price cannot be lower than 90% of the Expected Price!")

  def cancel_property(self):
    for record in self:
      if record.state == 'sold':
        raise UserError('Sold properties cannot be canceled.')

      record.state = 'canceled'
    return True

  def sell_property(self):
    for record in self:
      if record.state == 'canceled':
        raise UserError('Canceled properties cannot be sold.')

      record.state = 'sold'
    return True
