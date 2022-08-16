/**
 * シフト一括送信機能
 */
/*
function show_batch_sending_modal(){
    $('#batch_sending_Modal').modal('show');
}

function batch_sending(){
    const date_start_str = $('#date_start').val();
    const date_end_str = $('#date_end').val();
    const time_start = $('#time_start').val();
    const time_end = $('#time_end').val();

    console.log(date_start_str);

    //JSTの00:00として入力する
    date_start = new Date(Date.parse(date_start_str+"T00:00:00+09:00"));
    date_end = new Date(Date.parse(date_end_str+"T00:00:00+09:00"));
    console.log(date_start);
    console.log(date_end.getDate()-date_start.getDate()+1);

    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"

    for(let i=0;i<(date_end.getDate()-date_start.getDate()+1);i++){
        date = date_start
        axios
            .post('/SubmitShift-Ajax/',{
                'id':null,
                'date':$('#date').val(),
                'start':$('#start').val(),
                'end':$('#end').val()
            })
    }
}
*/