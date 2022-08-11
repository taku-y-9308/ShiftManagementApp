function draw_calender() {
    var calendarEl = document.getElementById('calendar');
    const eventData = JSON.parse(document.getElementById("event-data").textContent);
    var calendar = new FullCalendar.Calendar(calendarEl, {
      locale: 'ja',
      displayEventEnd :true,
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
      },
      navLinks: true, // can click day/week names to navigate views
      businessHours: true, // display business hours
      editable: true,
      selectable: true,
      eventBackgroundColor:'ff0000',
      eventTimeFormat:{
          hour: 'numeric',
          minute: '2-digit',
          meridiem: false
          },
        })
    }
