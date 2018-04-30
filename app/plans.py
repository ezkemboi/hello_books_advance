from flask_restful import Resource
import datetime
import uuid

from .models import Plan
from .user import token_required
from .parsers import plans_parser


class UserPlans(Resource):
    """Contain all plans that a user subscribe to"""
    @token_required
    def post(self, current_user, plan, category):
        """User chooses his/her plan according to needs"""
        plan = ['monthly', 'yearly']
        category = ['gold', 'diamond']
        args = plans_parser.parse_args()
        plan = args['plan']
        category = args['category']
        payment_date = datetime.datetime.now()
        monthly_expiry = payment_date + datetime.timedelta(days=30)
        yearly_expiry = payment_date + datetime.timedelta(days=365)
        if plan == 'monthly':
            if category == 'gold':
                charges = 17.99
                plan = Plan(plan_id=uuid.uuid4(), user_id=current_user.user_id,
                            unlimited_monthly_3=True, expiry=monthly_expiry, payment_date=payment_date,
                            charges=charges)
                plan.save_plans()
                return {"Message": "You have subscribed to monthly gold plan."}, 200
            elif category == 'diamond':
                charges = 29.99
                plan = Plan(plan_id=uuid.uuid4(), user_id=current_user.user_id,
                            unlimited_monthly_6=True, expiry=monthly_expiry, payment_date=payment_date,
                            charges=charges)
                plan.save_plans()
                return {"Message": "You have subscribed to monthly diamond plan."}, 200
        if plan == 'yearly':
            if category == 'gold':
                charges = 179.90
                plan = Plan(plan_id=uuid.uuid4(), user_id=current_user.user_id,
                            unlimited_yearly_3=True, expiry=yearly_expiry, payment_date=payment_date,
                            charges=charges)
                plan.save_plans()
                return {"Message": "You have subscribed to yearly gold plan."}, 200
            elif category == 'diamond':
                charges = 299.90
                plan = Plan(plan_id=uuid.uuid4(), user_id=current_user.user_id,
                            unlimited_yearly_6=True, expiry=yearly_expiry, payment_date=payment_date,
                            charges=charges)
                plan.save_plans()
                return {"Message": "You have subscribed to yearly diamond plan."}, 200
