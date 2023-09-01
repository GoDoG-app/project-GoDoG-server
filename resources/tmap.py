from flask import Response
from flask_restful import Resource
import requests

from config import Config


class TMapRouteResource(Resource):
    def post(self):
        # version= 1 or 2 (필수항목)
        url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&callback=function"

        payload = {
            # startX, startY, endY, endX, startName, endName (필수항목)
            # 출발 지점 : 연희직업전문학교
            "startX": 126.6772096,
            "startY": 37.5428428,
            # 각도 (0~ 359)
            "angle": 20,
            # 진행속도(km/h)
            "speed": 10,
            # 목적지의 POI ID
            "endPoiId": "10001",
            # 도착 지점 : 인천 아시아드 경기장
            "endX": 126.6772096,
            "endY": 37.5428428,
            # passList : 경유지 : 다이소-> 서구청
            # 위도와 경도의 구분은 콤마(,)이고,  장소간의 구분은 언더바(_)
            "passList": "126.6770159,37.5418009_126.6759938,37.5452851", 
            "reqCoordType": "WGS84GEO",
            "startName": "%EC%B6%9C%EB%B0%9C",
            "endName": "%EB%8F%84%EC%B0%A9",
            "searchOption": "0",
            "resCoordType": "WGS84GEO",
            "sort": "index"
        }
        # AppKey (필수항목)
        headers = {
            # 응답으로 받을 데이터의 형식
            # - application/json : json 포맷의 데이터 응답. (Default)
            # - application/xml: xml 포맷의 데이터 응답.
            # - application/javascript : jsonp 포맷의 데이터 응답
            "accept": "application/json",
            # 내가 보내는 데이터의 형식 json
            "content-type": "application/json",
            # 추후에 우리꺼로 바꿔야함 지금은 TMap 관리자 KEY
            "appKey": Config.TMAP_APP_KEY
        }        

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)



        # json 응답 1번
        response = response.json()
        return {"relsut" : "success",
                "items" : response}
        
        # # json 응답 2번
        # if response.status_code == 200:
        #     print(response.text)
        #     response = response.json()
            
        #     return {"result" : response}
        # else : 
        #     return "TMap API request Fialed", 500


#------------------------------------------------------

        # # xml 응답 1번
        # response = response.text
        # return {"relsut" : "success",
        #         "items" : response}

        # xml 응답 2번
        # if response.status_code == 200:
        # # API 응답을 XML로 변환하여 반환
        #     xml_response = response.text
        #     print(response.text)
        #     return Response(xml_response, content_type='application/xml')
        # else:
        #     return 'TMap API request Failed', 500