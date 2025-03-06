"""
@author: lijiahui
@version: V1.0
@file: add_house_service.py
@time: 2022/1/16
"""
import string
from random import random

from api_object.house.add_house import AddHouseAPI
from common.globalvar import GlobalVar
from common.readconfig import ini
from tools.mysql import select_sql

add_house_api = AddHouseAPI()

class AddHouseService(object):

    @staticmethod
    def get_house_info(flag='sale'):
        """获取conf文件中房源相关信息"""
        estate_sql = "select id from estate_new_base_info where name='" + ini.house_estate_name + "' and is_valid=1"
        GlobalVar.house_estate_id = str(select_sql(estate_sql)[0][0])
        building_number_sql = "select id from estate_new_block where estate_id='" + GlobalVar.house_estate_id \
                              + "' and block_index='" + ini.house_building_number + "' and is_valid=1"
        GlobalVar.house_building_number_id = str(select_sql(building_number_sql)[0][0])
        building_cell_sql = "select id from estate_new_block_cell where estate_id='" + GlobalVar.house_estate_id \
                            + "' and block_id='" + GlobalVar.house_building_number_id + "' and unit='" \
                            + ini.house_building_cell + "' and is_valid=1"
        GlobalVar.house_building_cell_id = str(select_sql(building_cell_sql)[0][0])
        location_sql = "select id from estate_new_cell_house where estate_id='" + GlobalVar.house_estate_id \
                       + "' and block_cell_id='" + GlobalVar.house_building_cell_id + "' and house_number='" \
                       + ini.house_doorplate + "' and is_valid=1"
        GlobalVar.house_location_id = str(select_sql(location_sql)[0][0])
        house_sql = "select id,house_code,status from @house_table where location_estate_id='" \
                    + str(GlobalVar.house_estate_id) + "' and location_building_number='" \
                    + ini.house_building_number + "' and location_building_cell='" + ini.house_building_cell \
                    + "' and location_floor='" + ini.house_floor + "' and location_doorplate='" \
                    + ini.house_doorplate + "' and status!='1' and is_valid='1'"
        if flag == 'sale':
            house_sql = house_sql.replace('@house_table', 'trade_house')
        elif flag == 'rent':
            house_sql = house_sql.replace('@house_table', 'rent_house')
        else:
            raise ValueError('传值错误')
        try:
            house_info = select_sql(house_sql)[0]
            return str(house_info[0]), house_info[1], house_info[2]
        except IndexError:
            return None

    def add_house(self, house_estate_id, house_building_number_id, house_building_cell, house_floor, house_doorplate,
                  house_location_id, flag='sale'):
        """新增房源"""
        params = {
            'locationInfo': {
                'communityId': house_estate_id,
                'buildingId': house_building_number_id,
                'buildingCell': house_building_cell,
                'floor': house_floor,
                'doorplate': house_doorplate,
                'locationId': house_location_id
            },
            'ownerInfo': {
                'name': "露露" + "".join(map(lambda x: random.choice(string.digits), range(2))),
                'phoneNumber': "".join(map(lambda x: random.choice(string.digits), range(11)))
            }
        }
        if flag == 'sale':
            add_house_api.add_preowned_house_request(params)
        elif flag == 'rent':
            add_house_api.add_rent_house_request(params)
        else:
            raise ValueError('传值错误')
        return self.get_house_info(flag)