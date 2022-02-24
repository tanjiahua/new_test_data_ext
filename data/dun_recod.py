# coding=utf-8
# author= 'Jack'
# time：2021/11/12

from common import test_mysql as db

def dun_recod():
    i=0;
    while i<10000:
        i=i+1
        env_mark = 'mx'
        sql = "INSERT INTO `mx_cfs`.`dun_record`(`order_id`, `user_id`, `dun_user_id`, `dun_user_name`, `dun_user_nick`, `contact_name`, `contact_mobile`, `remark`, `contact_relation`, `create_time`, `update_time`, `tag_ids`, `back_tag_ids`, `contact_results_value`, `collection_results_value`, `ptp_stay_fail_time`, `new_contact_relation`) VALUES ('1439115432436961280', '4952213673817022464', 1319, 'tanjiahua4', 'tanjiahua4', 'Duke', '01856496868', '222', 'ADDRESS_BOOK', '2021-11-11 23:58:03', '2021-11-11 23:58:03', NULL, NULL, '发送失败', 'RTP', NULL, 'ADDRESS_BOOK');"
        db.insert(sql,env_mark)


dun_recod()