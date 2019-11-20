# RreserveD
2019-2 SIT32006 TEAM PROJECT

일반사용자가 신청함 -> 자신의 id는 알고 있음. -> current_user
일반사용자가 3D 프린터를 선택할 수 있게 할 것인가? -> 없음

3D 프린팅 신청을 받으면 # get total count of the tasks(tot_count = …)
관리자에게 메일을 보내기 (task_id를 토큰으로)
관리자가 confirm을 누르면 progress collection에서 task_id를 찾음
task_id를 찾으면 장비 기입, estimation date 등 정보 기입 -> 관리자 권한
관리자 페이지-> @login_required @is_administrator 정보 받기
confirmed=false -> True으로 update -> submit 버튼을 누르면
사용자에게 메일
<table>
  <td><b>blueprint</b>
    <tr>auth</tr>
  </td>
