<h1># RreserveD</h1>
<h2>2019-2 SIT32006 TEAM PROJECT</h2>

1.일반사용자가 신청함 -> 자신의 id는 알고 있음. -> current_user

2.일반사용자가 3D 프린터를 선택할 수 있게 할 것인가? -> 없음

<h3>Process FLOW</h3>
<b>ToDO</b><br>
3D 프린팅 신청을 받으면 # get total count of the tasks(tot_count = …)

관리자에게 메일을 보내기 (task_id를 토큰으로)

관리자가 confirm을 누르면 progress collection에서 task_id를 찾음

task_id를 찾으면 장비 기입, estimation date 등 정보 기입 -> 관리자 권한

관리자 페이지-> @login_required @is_administrator 정보 받기

confirmed=false -> True으로 update -> submit 버튼을 누르면

사용자에게 메일

<h3>Page Design</h3>

<table>
  <tr>
    <td><b>blueprint</b></td>
      <td><b>route</b></td>
          <td><b>variable</b></td>
              <td><b>Jinja2 template</b></td>
                  <td><b>arguments</b></td>

  </tr>
  <tr>
    <td> auth</td>
    <td> login</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td> </td>
    <td> register</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  
  <tr>
    <td> </td>
    <td>confirm</td>
    <td>(token)</td>
    <td></td>
    <td></td>
  </tr>
  
  <tr>
    <td><b>main</b> </td>
    <td>request</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td></td>
    <td>check</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td></td>
    <td>confirm</td>
    <td>(task_id)</td>
    <td></td>
    <td></td>
  </tr>
  
  <tr>
    <td><b>manage</b> </td>
    <td>equip</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
 <tr>
    <td></td>
    <td>user</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td></td>
    <td>tasks</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
