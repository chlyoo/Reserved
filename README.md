<h1># RreserveD</h1>
<h2>2019-2 SIT32006 TEAM PROJECT</h2>
<h3>Admin Function</h3>
<li>Register Equips</li>
<li>Delete Equips</li>
<li>Modify Equips</li>
<li>Confirm</li>
<li>Complete</li>
<li>Paid</li>

<h3>Process FLOW</h3>
<1> 일반사용자가 장비를 예약함
<ul>사용자가 예약 취소 가능</ul>
<ul>사용자 예약 내역 확인 가능</ul>
<ul>관리자에게 메일 발송</ul>

<2>관리자가 파일을 확인하고 Confirm
<ul>예상시간과 예상가격을 입력하고 예약 Confirm</ul>
<ul>사용자에게 Confirm 완료 메일 발송 </ul>

<3>관리자가 작업이 완료되어 Complete
<ul>사용자에게 작업 완료 메일 발송</ul>

<4>이용비용 지급
<ul>관리자가 Paid 처리</ul>
<ul>프로세스 완료</ul>

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
               <td><b>Function</b></td>
                  <td><b>arguments</b></td>
                 

  </tr>
  <tr>
    <td> auth</td>
    <td>/login</td>
    <td></td>
    <td></td>
    <td>login</td><td></td>
    
 <tr>
    <td> </td>
    <td>/logout</td>
    <td></td>
    <td></td>
    <td>logout</td><td></td>
    
  </tr>
  </tr>
  <tr>
    <td> </td>
    <td>/register</td>
    <td></td>
    <td></td>
    <td>register</td><td></td>
    
  </tr>
  
  <tr>
    <td> </td>
    <td>/confirm</td>
    <td>(token)</td>
    <td></td>
    <td>confirm</td><td>(token)</td>
    
  </tr>
  
  <tr>
    <td><b>main</b> </td>
    <td>/</td>
    <td></td>
    <td></td>
    <td>index</td><td></td>
    
  </tr>
 
  
  <tr>
    <tr>
    <td><b>manage</b></td>
    <td>/</td>
    <td></td>
    <td>manage/main.html
    <br>┗manage/All_progress.html
    <br>┗manage/All_equips.html
    <td>main</td><td></td>
        
  </tr>
  <tr>
    <td></td>
    <td>/confirm/token</td>
    <td>token</td>
    <td>manage/do_confrim.html</td>
    <td>confirm</td><td>(token)</td>
    
  </tr>
  <tr>
    <td></td>
    <td>/complete/taskid</td>
    <td>taksid</td>
    <td></td>
    <td>complete</td><td>(taskid)</td>
    
  </tr>
  
 <tr>
    <td></td>
    <td>/paid/taskid</td>
    <td>taskid</td>
    <td></td>
    <td>pay</td><td>(taskid)</td>
    
  </tr>
  <tr>
    <td></td>
    <td>/register</td>
    <td></td>
    <td>manage/register_equip.html</td>
    <td>register_equip</td><td></td>
    
  </tr>
    <tr>
    <td></td>
    <td>/modify</td>
    <td></td>
    <td>manage/modify_equip.html</td>
    <td>modify_equip</td><td></td>
    
  </tr>
      <tr>
    <td></td>
    <td>/delete</td>
    <td></td>
    <td>manage/delete_equip.html</td>
    <td>delete_equip</td><td></td>
    
  </tr>
  <tr>
  <td></td>
  <td>/resource/filename</td>
  <td>filename</td>
  <td></td>
  <td>equipimage</td><td>(filename)</td>
  
  
  </tr>
 <tr>
    <td><b>reserve</b></td>
    <td>/reserve</td>
    <td></td>
    <td>reserve/reserve_selectequip.html</td>
    <td>select_equip</td><td></td>
    
  </tr>
  <tr>
    <td></td>
    <td>/equipid/table</td>
    <td>equipid</td>
<td>reserve/rdatetable.html
    </td>
    <td>table</td><td>(equipid)</td>
    
  </tr>
    <tr>
    <td></td>
    <td>/equipid/d/nwtable</td>
    <td>equipid</td>
    <td>reserve/rdatetable.html
    </td>
    <td>tablenext</td><td>(equipid)</td>
    
  </tr>
      <tr>
    <td></td>
    <td>/equipid/d/pwtable</td>
    <td>equipid</td>
    <td>reserve/rdatetable.html
    </td>
    <td>tableprevious</td><td>(equipid)</td>
    
  </tr>
   <tr>
    <td></td>
    <td>/equipid/datetimeval</td>
    <td>equipid<br></br>datetimeval</td>
    <td>reserve/reserve_main.html</td>
    <td>set_rdate</td><td>(equipid,datetimeval)</td>
  </tr>
   <tr>
    <td></td>
    <td>/workspace/filename</td>
    <td>filename</td>
    <td></td>
    <td>workfile</td><td>(filename)</td>
    
  </tr>
 
   <tr>
    <td><b>mypage</b></td>
    <td>/</td>
    <td></td>
    <td>mypage/myreserve.html<br>mypage/noreservation.html</td>
    <td>show_reservation</td><td></td>
    
  </tr>
 <tr>
    <td></td>
    <td>/cancel/taskid</td>
    <td>taskid</td>
    <td></td>
    <td>cancel</td><td>(taskid)</td>
  </tr>
<tr>
    <td></td>
    <td>/edit-profile</td>
    <td></td>
    <td>mypage/edit_profile.html</td>
    <td>edit_profile</td><td></td>
 
  </tr>
