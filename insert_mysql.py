import json
import pymysql
from datetime import datetime

def import_grid_data():
    # 数据库配置
    db_config = {
        'host': '223.107.76.174',
        'port': 13306,
        'user': 'misboot_xb',
        'password': 'AXdz2xCb784TEfpj',
        'database': 'misboot_xb',
        'charset': 'utf8mb4'
    }
    
    try:
        # 读取网格员数据
        with open('D:\project\天翼服务器备份\网格员.txt', 'r', encoding='utf-8') as file:
            grid_data = json.load(file)
        
        print(f"成功读取 {len(grid_data)} 条网格员数据")
        
        # 连接数据库
        connection = pymysql.connect(**db_config)
        
        try:
            with connection.cursor() as cursor:
                # 准备插入SQL
                insert_sql = """
                INSERT INTO t_home_information (
                    uuid, creator_id, creator, create_time, modifier_id, modifier, 
                    modify_time, creator_org_id, deleted, grid_color, population, 
                    households, grid_leader, phone, features, key_units, polygon
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """
                
                success_count = 0
                
                for item in grid_data:
                    try:
                        # 处理时间格式转换
                        create_time = None
                        modify_time = None
                        
                        if item.get('createTime'):
                            create_time = item['createTime'].replace('T', ' ').split('.')[0]
                        if item.get('modifyTime'):
                            modify_time = item['modifyTime'].replace('T', ' ').split('.')[0]
                        
                        # 执行插入
                        cursor.execute(insert_sql, (
                            item.get('uuid'),
                            item.get('creatorId'),
                            item.get('creator'),
                            create_time,
                            item.get('modifierId'),
                            item.get('modifier'),
                            modify_time,
                            item.get('creatorOrgId'),
                            item.get('deleted', 0),
                            item.get('gridColor'),
                            item.get('population'),
                            item.get('households'),
                            item.get('gridLeader'),
                            item.get('phone'),
                            item.get('features'),
                            item.get('keyUnits'),
                            item.get('polygon')
                        ))
                        success_count += 1
                        
                    except Exception as e:
                        print(f"插入数据失败: {item.get('uuid')}, 错误: {str(e)}")
                        continue
                
                # 提交事务
                connection.commit()
                print(f"数据导入完成! 成功插入 {success_count} 条记录")
                
        except Exception as e:
            print(f"数据库操作失败: {str(e)}")
            connection.rollback()
            
        finally:
            connection.close()
            
    except FileNotFoundError:
        print("错误: 找不到 '网格员.txt' 文件")
    except json.JSONDecodeError:
        print("错误: '网格员.txt' 文件格式不正确")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    import_grid_data()