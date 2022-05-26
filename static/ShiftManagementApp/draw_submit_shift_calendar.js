/*カレンダー描画***********/
document.addEventListener('DOMContentLoaded', function draw_calender() {
    var calendarEl = document.getElementById('calendar');
    let eventData = JSON.parse(document.getElementById("event-data").textContent);
    let start_date = document.getElementById("start_date").textContent.replace(/"/g,'');
    let end_date = document.getElementById("end_date").textContent.replace(/"/g,'');
    console.log(typeof(start_date));
    console.log(start_date);
    var calendar = new FullCalendar.Calendar(calendarEl, {
      validRange: {
          start: start_date,
          end: end_date
      },
      locale: 'ja',
      displayEventEnd :true,
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'listMonth,dayGridMonth,timeGridWeek'
      },
      dayCellContent: function (e) {
          e.dayNumberText = e.dayNumberText.replace('日', '');
      },
      eventDisplay:'block',
      navLinks: false, // can click day/week names to navigate views
      editable: true,
      selectable: true,
      eventBackgroundColor:'ff0000',
      contentHeight: 'auto',
      selectLongPressDelay:0,
      eventTimeFormat:{
          hour: 'numeric',
          minute: '2-digit',
          omitZeroMinute: true,
          meridiem: 'narrow'
          },
  
      eventClick: function (info){ //イベントクリックで実行
          axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
          axios.defaults.xsrfCookieName = "csrftoken"
          const date = moment(info.event.start).format('YYYY-MM-DD');
          const start = moment(info.event.start).format('HH:mm');
          const end = moment(info.event.end).format('HH:mm');
          $('#shift_id').val(info.event.id)//shiftのidはイベントのid
          $('#date').val(date);
          $('#start').val(start);
          $('#end').val(end);
          $('#testModal').modal('show');
  
          /*送信ボタン押下時*/
          $('#submit').off('click') //offでクリックイベントを削除することで複数登録を防ぐ
          $('#submit').click(function(){
              //イベント追加する時使うためidは保持しておく
              let shift_id = info.event.id;
              axios
                  .post("/SubmitShift-Ajax/",{
                      'date':$('#date').val(),
                      'start':$('#start').val(),
                      'end':$('#end').val(),
                      'id':shift_id
                  })
                  .then((res)=>{
  
                      if(res.data[0]['res_code']==true){
                          console.log(typeof(res.data));
                          //calendar.getEventSources().remove();
                          $('#testModal').modal('hide'); //modalを閉じる
                          //新しいeventDataを取得
                          eventData = res.data
                          alert("送信されました")
                      }else{
                          console.log('else')
                          alert("編集可能期間が過ぎているため編集できません")
                      }
                      
                  })
                  .catch(()=>{
                      alert("送信失敗しました。再読み込みしてください");
                  })
                  let event = calendar.getEventById($('#shift_id').val())
                  event.remove();
                  console.log(typeof 42)
                  calendar.addEvent({
                  id : shift_id,
                  start : $('#date').val()+"T"+$('#start').val(),
                  end : $('#date').val()+"T"+$('#end').val(),
                  borderColor : '#ff0000',
                  })
                  calendar.render();
                  /*
                  calendar.addEvent({
                  id : $('#shift_id').val(),
                  start : $('#start').val(),
                  end : $('#end').val(),
                  borderColor : '#ff0000',
              });
              */
              
          /*削除ボタン押下時*/
          })
          $('#delete-shift').off('click');
          $('#delete-shift').click(function(){
              axios
                  .post("/edit-shift-Ajax/delete-shiftdata/",{
                      'id':$('#shift_id').val(),
                      'start':$('#start').val()
                  })
                  .then((res)=>{
                      console.log(res.data);
                      console.log($('#shift_id').val())
                      //削除可能期間内の場合
                      if(res.data[0]['res_code']==true){
                          //calendar.getEventSources().remove();
                          alert("削除しました");
                          //新しいeventDataを取得
                          eventData = res.data
                          //カレンダー再描画
                          let event = calendar.getEventById($('#shift_id').val())
                          event.remove();
                          calendar.render();
                      }else{
                          alert("削除可能期間外のため削除できません");
                      }
                      
                  })
                  .catch(()=>{
                      alert("送信失敗しました。再読み込みしてください");
                  })
                  .finally(()=>{
                      $('#testModal').modal('hide'); //modalを閉じる
                  });
          })
      },
      //日付の枠クリックで実行される
      select: function (info) {
          axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
          axios.defaults.xsrfCookieName = "csrftoken"
  
          const day = moment(info.start).format('YYYY-MM-DD');//momentとformatで指定の方に変換
          const start_end_time =moment(info.start).format('YYYY-MM-DDTHH:mm');
          
          /*modalの値を初期化*/
          $('#shift_id').val('');
          $('#date').val(day);//formのid=dateの場所(今回は日付)に出力 
          $('#start').val(start_end_time);
          $('#end').val(start_end_time);
          $('#testModal').modal('show');//指定のidのモーダルを表示
          $('#submit').off('click') //offでクリックイベントを削除することで複数登録を防ぐ
          $('#submit').click(function(){
              axios
                  .post("/SubmitShift-Ajax/",{
                      'id':null,
                      'date':$('#date').val(),
                      'start':$('#start').val(),
                      'end':$('#end').val()
                  })
                  .then((res)=>{
                      $('#testModal').modal('hide'); //modalを閉じる
                      console.log(res.data[0]['res_code']==true);
                      if(res.data[0]['res_code']==true){
                          console.log('true');
                          let shift_id = res.data[0]['shift_id'];
                          //カレンダーに新しいイベントを追加
                          calendar.addEvent({
                              id : shift_id,
                              start : $('#date').val()+"T"+$('#start').val(),
                              end : $('#date').val()+"T"+$('#end').val(),
                              borderColor : '#ff0000',
                          });
                          alert("送信されました");   
                      }else{
                          console.log('else')
                          alert("編集可能期間外のため編集できません")
                      }
                  })
                  .catch((error)=>{
                          console.log(error.response);
                          alert("送信失敗しました。再読み込みしてください。");
                      })
                 
              
          });
      },
      events: eventData,
    });
  
    calendar.render();
  });