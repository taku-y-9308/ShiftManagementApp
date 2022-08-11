function get_holidays_list(holidays_list){
    const eventDates = [];

    holidays = Object.keys(holidays_list)
    for(let i=0;i<holidays.length;i++){
        holiday = {
            id: holidays[i],
            title: holidays_list[holidays[i]],
            start: holidays[i]+"T00:00:00Z",
            end: holidays[i]+"T00:00:00Z",
            allDay: true,
            editable: false,

        }
        eventDates.push(holiday)
    }
    return eventDates
}