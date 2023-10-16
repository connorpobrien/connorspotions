from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import math
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/inventory")
def get_inventory():
    """ """
    # Get values from database
    with db.engine.begin() as connection:
        # get data from global_inventory
        sql_query = """SELECT gold, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml FROM global_inventory"""
        global_inventory = connection.execute(sqlalchemy.text(sql_query))
        gold, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml = global_inventory.first()
        total_ml = num_red_ml + num_green_ml + num_blue_ml + num_dark_ml

        # Get data from catalog
        sql_query = """SELECT SUM(quantity) AS total_potions FROM catalog"""
        total_potions = connection.execute(sqlalchemy.text(sql_query)).first().total_potions
    
    return {"number_of_potions": total_potions, "ml_in_barrels": total_ml, "gold": gold}

class Result(BaseModel):
    gold_match: bool
    barrels_match: bool
    potions_match: bool

# Gets called once a day
@router.post("/results")
def post_audit_results(audit_explanation: Result):
    """ """
    print(audit_explanation)

    return "OK"
