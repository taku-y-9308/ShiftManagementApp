window.addEventListener('DOMContentLoaded',account_setting)

function account_setting() {
    const tableEle = document.getElementById('account_setting_table');
    const tbody = document.getElementById('table_body');
    tbody.innerHTML = "";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"
    dispLoading('Loading...');
    axios
        .post('/account-setting/',{})
        .then((res)=>{
            console.log(res.data);

            for(let i_person=0;i_person<res.data.length;i_person++){
                const tr = document.createElement('tr');
                const td_user_id = document.createElement('td');
                const td_username = document.createElement('td');
                const td_default_position = document.createElement('td');
                const td_is_active = document.createElement('td');
                const td_is_edit_mode = document.createElement('td');
                const td_is_delete = document.createElement('td');
                
                td_user_id.innerHTML = res.data[i_person].user_id;
                tr.appendChild(td_user_id);
                console.log(res.data[i_person].user_id);

                td_username.innerHTML = res.data[i_person].username;
                tr.appendChild(td_username);
                
                if(res.data[i_person].default_position){
                    td_default_position.innerHTML = '<span class="h6"><b>ホール</b></span>';    
                }else{
                    td_default_position.innerHTML = '<span class="h6"><b>キッチン</b></span>';    
                }
                tr.appendChild(td_default_position);

                /**アクティベートされているかどうか判定 */
                if(res.data[i_person].is_active){
                    td_is_active.innerHTML = '<button type="button" class="btn btn-success">有効</button>';
                    
                }else{
                    td_is_active.innerHTML = '<button type="button" class="btn btn-danger">無効</button>';
                }
                td_is_active.onclick = function () {
                    valid_invalid_change(res.data[i_person].user_id,'is_active',res.data[i_person].is_active);
                }
                tr.appendChild(td_is_active);
                
                /**シフト編集モードがONかOFFかを判定 */
                if(res.data[i_person].is_edit_mode){
                    td_is_edit_mode.innerHTML = '<button type="button" class="btn btn-danger">有効</button>';
                }else{
                    td_is_edit_mode.innerHTML = '<button type="button" class="btn btn-secondary">無効</button>';
                }
                td_is_edit_mode.onclick = function(){
                    valid_invalid_change(res.data[i_person].user_id,'is_edit_mode',res.data[i_person].is_edit_mode);
                }
                tr.appendChild(td_is_edit_mode);

                /**ユーザーを削除するボタンを表示 */
                td_is_delete.innerHTML = '<img src="/static/ShiftManagementApp/delete_icon.svg" width="35px">'
                td_is_delete.onclick = function(){
                    const confirm_mes = '<p>本当に削除しますか？</p><p>ユーザーを削除すると関連するシフトも完全に削除されます</p><p><span style="color:red;"><b>※削除したアカウントは復元できません</b></span></p>'
                    bootbox.confirm(confirm_mes, function (result) {
                        if (result) {
                            valid_invalid_change(res.data[i_person].user_id,'is_delete',true);
                        } else {
                        }
                    });
                    //const delete_confilm = confirm('削除しますか？')
                    //valid_invalid_change(res.data[i_person].user_id,'is_delete',true);
                }

                tr.appendChild(td_is_delete);

                tbody.appendChild(tr);
                
            }
            

        })
        .catch((res)=>{
            console.log(res);
        })
        .finally(()=>{
            removeLoading();
        })
}
window.globalFunction = {};
window.globalFunction.account_setting = account_setting;