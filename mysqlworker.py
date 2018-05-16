import urllib.parse

class ManagerSQL:
    def __init__(self, dbConfig):
        '''
        Принимает параметры для подключения
        к базе данных
        '''
        self.dbConfig=dbConfig
        
    def _CreateRequestSQL(self, req, isRet=True):
        import mysql.connector
        conn=mysql.connector.connect(**self.dbConfig)
        cursor=conn.cursor()
        cursor.execute(req)
        if(isRet):
            data=cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            return data
        conn.commit()
        cursor.close()
        conn.close()

class User(ManagerSQL):
    def _ConvertUrlToStr(self,url):
        url_convert=urllib.parse.parse_qs(url)
        return url_convert
    
    def _MakeOrder(self,order_str):
        price=0
        temp_price=0
        products=""
        orderArray=[]
        
        for key in order_str.keys():
            
            if '[price]' in key:
                temp_price=int(order_str[key][0])

            if '[title]' in key:
                products+=order_str[key][0]
            
            if '[count]' in key:
                price+=temp_price*int(order_str[key][0])
                products+='('+order_str[key][0]+')\n'
        orderArray.append(products)
        orderArray.append(price)
        return orderArray
    
    def Buy(self, order_str, user_data):
        user=self._ConvertUrlToStr(user_data)
        order=self._MakeOrder(self._ConvertUrlToStr(order_str))
               
        req_order='insert into orders (products, price, date) values("'+str(order[0])+'","'+str(order[1])+'", NOW());'
        req_user='insert into buyer (name, address, phone, mail, comment, id_order) value('
        req_user+='"'+user['user_name'][0]
        req_user+='" ,"'+user['user_address'][0]
        req_user+='" ,"'+user['user_phone'][0]
        req_user+='" ,"'+user['user_mail'][0]
        req_user+='" ,"'+user['user_comment'][0]
        req_user+='" ,'+str(1)+');'
        
        self._CreateRequestSQL(req_order, isRet=False)
        self._CreateRequestSQL(req_user, isRet=False)

class Admin(ManagerSQL):

    def _GetCategorieId(self, name):
        req='select id from categories where name='+name+';'
        data=self._CreateRequestSQL(req)
        cat_id=data[0][0]
        return cat_id
    
    def GetLoginAndPass(self):
        sql_req='''select* from admin;'''
        data=self._CreateRequestSQL(sql_req)
        return data[0][0]+data[0][1]
    
    def AddProduct(self, parametrs):
        sql_req='''insert into products'
                       '(name, discription, cattigory_id,
                       'availability, image, price)
                       'value (%s,%s,select id from c where cat_name=%s,
                       %s,%s,%s);'''
        self._CreateRequestSQL((sql_req,parametrs), isRet=False)
       
        
    def DeletProduct(self,id_number):
        sql_req='delete from products where id='+str(id_number)
        self._CreateRequestSQL(sql_req, isRet=False)
        
    def CheckOrders(self):
        sql_req='select * from orders'
        return self._CreateRequestSQL(sql_req)

    def RebuildProduct(self, field, val, id_numb):
        sql_req='update products set'+field+'='+str(val)+' where id='+str(id_numb)
        self._CreateRequestSQL(sql_req, isRet=False)

    def DeleteCategory(self, id_numb):
        sql_req='delete from categories where id='+id_numb
        self._CreateRequestSQL(sql_req, isRet=False)

    def AddCategory(self, name_cat):
        sql_req='insert into categories name value('+cat_name+');'
        self._CreateRequestSQL(sql_req, isRet=False)
    
    def FlagAnOrder(self):
        '''Изменить статус заказа выполнен или не выполнен'''
        pass

class Shop(ManagerSQL):
    def GetCategorys(self):
        req_sql='''select name from categories'''
        categorys=[]
        for cat in self._CreateRequestSQL(req_sql):
            categorys.append(cat[0])
        return categorys

    def GetProducts(self):
        req_sql='''select* from products'''
        products=self._CreateRequestSQL(req_sql)
        return products
