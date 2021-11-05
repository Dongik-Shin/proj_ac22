
from config.config import Config


class Mysql:

    def __init__(self):
        config = Config()
        conn = config.set_mysql()

        self.conn = conn
        self.cursor = conn.cursor()
        self.fetch_result = None

    def format_read_one(self):
        """ read_one 포멧팅

        Returns
        -------
        row_dict: 포멧 데이터 (dict) 
        """

        row_dict = {}
        for idx, row in enumerate(self.fetch_result):
            row_dict[self.cursor.description[idx][0]] = row

        return row_dict

    def read_one(self, query, bind=None):
        """ 데이터 단일 조회 

        Parameters : 
        query: 쿼리문(str) 
        bind : 바인드(tuple)

        Returns
        -------
        response_object : 결과 오브젝트 (dict)
        """

        try:
            # 쿼리 실행
            if bind:
                self.cursor.execute(query, bind)

            else:
                self.cursor.execute(query)

            # 데이터 조회 및 결과 리턴
            self.fetch_result = self.cursor.fetchone()
            if self.fetch_result != None:
                response_object = {
                    "status": "success",
                    "message": "success",
                    "row": self.format_read_one()
                }
                return response_object

            else:
                response_object = {
                    "status": "no_data",
                    "message": "no_data",
                    "row": None
                }
                return response_object

        except Exception as ex:
            response_object = {
                "status": "fail",
                "message": str(ex)
            }
            return response_object

        finally:
            self.conn.close()
            self.fetch_result = None

    def format_read_all(self):
        """ read_all 포멧팅

        Returns
        -------
        row_list : 포멧 데이터(list)
        """

        row_list = []
        for idx, rows in enumerate(self.fetch_result):

            row_dict = {}
            for idx2, row in enumerate(rows):
                row_dict[self.cursor.description[idx2][0]] = row

            row_list.append(row_dict)

        return row_list

    def read_all(self, query, bind=None):
        """ 데이터 복수 조회 

        Parameters : 
        query : 쿼리문(str) 

        Returns
        -------
        response_object : 결과 오브젝트(dict)
        """

        try:
            # 쿼리 실행
            if bind:
                self.cursor.execute(query, bind)

            else:
                self.cursor.execute(query)

            # 데이터 조회 및 결과 리턴
            self.fetch_result = self.cursor.fetchall()
            if self.fetch_result != None:
                response_object = {
                    "status": "success",
                    "message": "success",
                    "rows": self.format_read_all()
                }
                return response_object

            else:
                response_object = {
                    "status": "no_data",
                    "message": "no_data",
                    "rows": None
                }
                return response_object

        except Exception as ex:
            response_object = {
                "status": "fail",
                "message": str(ex)
            }
            return response_object

        finally:
            self.conn.close()
            self.fetch_result = None

    def excute_query(self, query=None, query_bulk=None):
        """ 쿼리 실행

        Parameters : 
        query : 쿼리문 단일(str)
        query_bulk : 쿼리문 배열(list)

        Returns
        -------
        response_object(dict) : 결과 오브젝트 
            ㄴlastrowids : 인서트 된 pk 배열(list)
        """

        try:
            lastrowids = []

            if query or query_bulk:

                # 단일 케이스
                if query:
                    self.cursor.execute(query)
                    if str(query.lower()).find("insert") >= 0:
                        lastrowids.append(self.cursor.lastrowid)

                # 복수 케이스
                elif query_bulk:
                    for query in query_bulk:
                        self.cursor.execute(query)

                        if str(query.lower()).find("insert") >= 0:
                            lastrowids.append(self.cursor.lastrowid)

                self.conn.commit()

            response_object = {
                "status": "success",
                "message": "success",
                "lastrowids": lastrowids
            }
            return response_object

        except Exception as ex:
            self.conn.rollback()
            response_object = {
                "status": "fail",
                "message": str(ex)
            }
            return response_object

        finally:
            self.conn.close()
