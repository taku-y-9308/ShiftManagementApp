/**
 * シフト一括送信機能
 */

function show_batch_sending_modal(){
    $('#batch_sending_Modal').modal('show');
}

function batch_sending(){

    dispLoading('サーバーへ送信中...');
    
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
    
    const diff_start_end = date_end.getDate()-date_start.getDate()+1;
    for(let i=0;i<diff_start_end;i++){
        

        //0埋めする
        const year = date_start.getFullYear();
        const month = ('0'+ (date_start.getMonth()+1)).slice(-2);
        const date = ('0' + date_start.getDate()).slice(-2);
        const date_for_post = year+"-"+month+"-"+date;


        axios
            .post('/SubmitShift-Ajax/',{
                'id':null,
                'date':date_for_post,
                'start':$('#batch_sending_start').val(),
                'end':$('#batch_sending_end').val()
            })
            .then((res)=>{
                console.log(res);
                const shift_id = res.data[0].shift_id;
                window.calendar.addEvent({
                id : shift_id,
                start : date_for_post+"T"+$('#batch_sending_start').val(),
                end : date_for_post+"T"+$('#batch_sending_end').val(),
                borderColor : '#ff0000',
                })
                calendar.render();

            })
            .catch((res)=>{
                console.log(res);
                alert('送信失敗しました。再読み込みして確認してください')
            })
            .finally(()=>{
                $('#batch_sending_Modal').modal('hide');
                removeLoading();                
            })
        
        date_start.setDate(date_start.getDate()+1);
    }

}
