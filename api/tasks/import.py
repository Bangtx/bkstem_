import csv
import uuid
import click
from models.item import Item
from models.variety import Variety
from models.unit import Unit
from models.customer import Customer
from utils.mecab import get_pronunciation, normalize_text
from config.database import db


@click.group("import")
def cli():
    """Import master data from csv file"""


@cli.command("jfd")
@click.option(
    "-t",
    "--table",
    required=True,
    help="Master table",
)
@click.option(
    "-f",
    "--file",
    required=True,
    help="File csv",
)
def cli_jfd(table, file):
    """
    Import master table for jfd

    Example:
        \b
        task import jfd \\
            --table 'item' \\
            --file 'item.csv'
    """

    my_task = TaskImport
    if table == "item":
        my_task(file).insert_item()

    if table == "variety":
        my_task(file).insert_variety()

    if table == "customer":
        my_task(file).insert_customer()

    # reset_sequence(table)


def is_exists(data, list_data):
    return data in list_data


def get_id_by_name(name, list_id, list_name):
    if is_exists(name, list_name):
        return list_id[list_name.index(name)]
    return None


def get_size_group_by_id(id, list_id, list_size):
    if is_exists(id, list_id):
        return list_size[list_id.index(id)]
    return None


class TaskImport:
    def __init__(self, file):
        # open file
        csv_file = open(f"tasks/{file}", encoding="shift-jisx0213")
        reader = csv.reader(csv_file, delimiter=",")

        # read header file
        try:
            next(reader)
        except Exception:
            try:
                csv_file = open(f"tasks/{file}", encoding="utf-8")
                reader = csv.reader(csv_file, delimiter=",")
                next(reader)
            except Exception:
                print("file error (file csv utf-8 or shift-jisx0213)")

        self.reader = list(reader)

    # NOTE: remove order_num due to newest request
    def insert_item(self):
        # insert unit if not exit
        # get all unit already in unit table
        all_unit = Unit.get_list()
        list_name_unit = [normalize_text(unit_.name) for unit_ in all_unit]
        list_id_unit = [unit_.id for unit_ in all_unit]

        for row in self.reader:
            unit_name = normalize_text(row[3])
            if unit_name is not None and unit_name != "":
                if not is_exists(unit_name, list_name_unit):
                    list_name_unit.append(unit_name)
                    unit_data = {
                        "name": unit_name,
                        "yomi": get_pronunciation(unit_name),
                        "search_str": Unit.gen_search_str(
                            name=unit_name, yomi=get_pronunciation(unit_name)
                        ),
                    }
                    id = Unit.insert(**unit_data).execute()
                    if id:
                        list_id_unit.append(id)

        # insert item if not exists
        # get all item already in item table
        all_item = Item.get_list()
        list_name_item = [normalize_text(item_.name) for item_ in all_item]
        list_id_item = [item_.name for item_ in all_item]

        for row in self.reader:
            item_name = normalize_text(row[1])
            unit_name = normalize_text(row[3])
            item_id = row[0]
            unit_id = get_id_by_name(unit_name, list_id_unit, list_name_unit)

            if item_name is not None and item_name != "":
                if not is_exists(item_name, list_name_item):
                    list_name_item.append(item_name)
                    item_data = {
                        "id": int(item_id),
                        "name": item_name,
                        "name_eng": None,
                        "short_name": None,
                        "yomi": get_pronunciation(item_name),
                        "default_unit": unit_id
                        if unit_id
                        else get_id_by_name("本", list_id_unit, list_name_unit),
                        "uuid": uuid.uuid4(),
                        "search_str": Item.gen_search_str(
                            name=item_name, yomi=get_pronunciation(item_name)
                        ),
                    }
                    id = Item.insert(**item_data).execute()
                    if id:
                        list_id_item.append(id)

    # NOTE: remove order_num due to newest request
    def insert_variety(self):
        # insert item if not exit
        # get all item already in item table
        all_item = Item.get_list()
        list_name_item = [normalize_text(item_.name) for item_ in all_item]
        list_id_item = [item_.id for item_ in all_item]
        list_size_group_id_item = list(map(lambda x: x.size_group.id, all_item))
        if all_item:
            last_id = all_item[-1].id + 1
        else:
            last_id = 1

        # get all variety already variety table
        all_variety = Variety.get_list()

        list_id_variety = [variety_.id for variety_ in all_variety]
        list_name_variety_id_item = list(map(lambda x: x.name + '_' + str(x.item_id), all_variety))

        # get all unit default
        all_unit = Unit.get_list()
        list_name_unit = [normalize_text(unit_.name) for unit_ in all_unit]
        list_id_unit = [unit_.id for unit_ in all_unit]
        id_unit_default = get_id_by_name("本", list_id_unit, list_name_unit)

        self.reader = list(self.reader)
        num_row = 0
        for row in self.reader:
            num_row += 1
            item_name = normalize_text(row[-2])
            item_id = get_id_by_name(item_name, list_id_item, list_name_item)
            variety_name = normalize_text(row[2])
            variety_id = int(row[0])
            # insert item if not exists
            if item_id is None:
                item_data = {
                    # not use id to prevent incorrect sequence
                    "name": item_name,
                    "name_eng": None,
                    "short_name": None,
                    "yomi": get_pronunciation(item_name),
                    "default_unit": id_unit_default,
                    "uuid": uuid.uuid4(),
                    "size_group": 1,
                    "search_str": Item.gen_search_str(
                        name=item_name, yomi=get_pronunciation(item_name)
                    ),
                }
                last_id += 1
                id = Item.insert(**item_data).execute()
                if id:
                    list_id_item.append(id)
                    list_name_item.append(item_name)
                    list_size_group_id_item.append(1)
            
            if not is_exists(variety_name + '_' + str(item_id), list_name_variety_id_item):
                item_id = get_id_by_name(item_name, list_id_item, list_name_item)
                variety_data = {
                    "id": variety_id,
                    "uuid": uuid.uuid4(),
                    "item_id": item_id,
                    "size_group": get_size_group_by_id(
                        item_id, list_id_item, list_size_group_id_item
                    ),
                    "quality_group": 1,
                    "short_name": variety_name,
                    "name": variety_name,
                    "yomi": get_pronunciation(variety_name),
                    "search_str": Variety.gen_search_str(
                        name=variety_name, yomi=get_pronunciation(variety_name)
                    ),
                }
                id = Variety.insert(**variety_data).execute()
                if id:
                    list_id_variety.append(id)
                    list_name_variety_id_item.append(variety_name + '_' + str(item_id))

    # NOTE: remove order_num due to newest request
    def insert_customer(self):
        # get all customer already insert
        all_customer = Customer.get_list()
        list_id_customer = [customer_.id for customer_ in all_customer]

        for row in self.reader:
            customer_id = int(row[0])
            customer_name = normalize_text(row[3])
            customer_short_name = normalize_text(row[1])
            customer_tel = normalize_text(row[8])
            customer_fax = normalize_text(row[9])
            customer_email = normalize_text(row[-3])

            if not is_exists(customer_id, list_id_customer):
                customer_data = {
                    "id": customer_id,
                    "name": customer_name,
                    "yomi": get_pronunciation(customer_name),
                    "short_name": customer_short_name,
                    "search_str": Customer.gen_search_str(
                        customer_name=customer_name,
                        yomi=get_pronunciation(customer_name),
                    ),
                    "tel": customer_tel,
                    "fax": customer_fax,
                    "email": customer_email,
                }
                id = Customer.insert(**customer_data).execute()
                if id:
                    list_id_customer.append(id)


def str_to_class(classname):
    import sys

    return getattr(sys.modules[__name__], classname)


def reset_sequence(table: str):
    model = str_to_class(table.title())
    items = model.select(model.id).order_by(model.id.desc()).limit(1).dicts()
    last_id = items[0]["id"]

    reset_id = last_id + 1
    query = f"alter sequence {table}_id_seq restart with {reset_id}"
    db.execute_sql(query)
