import GUI.constants as c
import yaml
import os

def check_money(acc_money, bid_money):
    if acc_money > bid_money:
        return c.RIGHT
    return c.FALSE

def check_name(acc_name, bid_name, def_color):
    color = c.BLUE if acc_name == bid_name else def_color
    return color

def yaml_loader():
        with open(os.getcwd() + "/" + c.AppShipValue, "r", encoding='utf-8') as stream:
            data = yaml.safe_load(stream)
            return data

def yaml_return_namelist():
    return [item['name'] for item in yaml_loader().values()]

def choose_ship_by_id(get_id):
    return yaml_loader().get("ship_"+get_id)