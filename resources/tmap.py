import json
from urllib import response
from flask import Response, jsonify, request
from flask_restful import Resource
import requests
from config import Config

class TMapRouteResource(Resource):
    def post(self):
        # 폼데이터를 받아온다.
        startX = request.form['startX']
        startY = request.form['startY']
        endX = request.form['endX']
        endY = request.form['endY']
        speed = request.form['speed']
        passList = request.form['passList']
        startName = request.form['startName']
        endName = request.form['endName']
        searchOption = request.form['searchOption']
        # version= 1 or 2 (필수항목)
        url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&callback=function"
        # payload = {
        #     # startX, startY, endY, endX, startName, endName (필수항목)
        #     # 출발 지점 : 연희직업전문학교
        #     "startX": startX,
        #     "startY": startY,
        #     # 각도 (0~ 359)
        #     "angle": 20,
        #     # 진행속도(km/h)
        #     "speed": speed,
        #     # 목적지의 POI ID
        #     # "endPoiId": "10001",
        #     # 도착 지점 : 인천 아시아드 경기장
        #     "endX": endX,
        #     "endY": endY,
        #     # passList : 경유지 : 다이소-> 서구청
        #     # 위도와 경도의 구분은 콤마(,)이고,  장소간의 구분은 언더바(_)
        #     "passList": passList,
        #     # "reqCoordType": "WGS84GEO",
        #     "startName": startName,
        #     "endName": endName,
        #     "searchOption": searchOption,
        #     # "resCoordType": "WGS84GEO",
        #     # "sort": "index"
        # }
        payload = {
            # startX, startY, endY, endX, startName, endName (필수항목)
            # 출발 지점 : 연희직업전문학교
            "startX": startX,
            "startY": startY,
            # 각도 (0~ 359)
            "angle": 20,
            # 진행속도(km/h)
            "speed": speed,
            # 목적지의 POI ID
            # "endPoiId": "10001",
            # 도착 지점 : 인천 아시아드 경기장
            "endX": endX,
            "endY": endY,
            # passList : 경유지 : 다이소-> 서구청
            # 위도와 경도의 구분은 콤마(,)이고,  장소간의 구분은 언더바(_)
            "passList": passList,
            "reqCoordType": "WGS84GEO",
            "startName": startName,
            "endName": endName,
            "searchOption": searchOption,
            "resCoordType": "WGS84GEO",
            "sort": "index"
        }
        # AppKey (필수항목)
        headers = {
            # 응답으로 받을 데이터의 형식
            # - application/json : json 포맷의 데이터 응답. (Default)
            # - application/xml: xml 포맷의 데이터 응답.
            # - application/javascript : jsonp 포맷의 데이터 응답
            "accept": "application/xml",
            # 내가 보내는 데이터의 형식 json
            "content-type": "application/json",
            # 추후에 우리꺼로 바꿔야함 지금은 TMap 관리자 KEY
            "appKey": Config.TMAP_APP_KEY
        }
        # response = requests.post(url, json=payload, headers=headers)
        # if response.status_code == 200:
        #     # API 응답을 JSON 형식으로 파싱
        #     response_text_cleaned = response.text.replace('\x00', '')  # 유효하지 않은 문자를 빈 문자열로 대체
        #     try:
        #         data = json.loads(response_text_cleaned)
        #     except json.JSONDecodeError as e:
        #         return jsonify({'error': 'JSON 디코드 오류 발생', 'message': str(e)})
        #     # distance, time 및 coordinates 정보 추출
        #     route_info = []
        #     for feature in data['features']:
        #         if feature['geometry']['type'] == 'LineString':
        #             distance = feature['properties']['distance']
        #             time = feature['properties']['time']
        #             coordinates = feature['geometry']['coordinates']
        #             route_info.append({
        #                 'distance': distance,
        #                 'time': time,
        #                 'coordinates': coordinates
        #             })
        #     # JSON 응답으로 반환
        #     return jsonify(route_info)
        # else:
        #     return jsonify({'error': 'API 요청 실패'})
        # # json 응답 1번
        # response = response.json()
        # return {"relsut" : "success",
        #         "items" : response}
        # # json 응답 2번
        # if response.status_code == 200:
        #     print(response.text)
        #     response = response.json()
        #     return {"result" : response}
        # else :
        #     return "TMap API request Fialed", 500
#------------------------------------------------------
        # xml 응답 1번
        # response = response.text
        # return {"relsut" : "success",
        #         "items" : response}
        # # xml 응답 2번
        if response.status_code == 200:
        # # API 응답을 XML로 변환하여 반환
            xml_response = response.text
            print(response.text)
            return Response(xml_response, content_type='application/xml')
        else:
            return 'TMap API request Failed', 500