# coding=utf-8
# author= 'Jack'
# time：2021/12/3

a=0
b = 1461
while a<50:
    a=a+1
    b=b+1
    s1='KX0'+ str(a)
    print("INSERT INTO `ke_cfs`.`tele_marketer_user`(`login_name`, `user_name`, `user_id`, `mobile`, `status`, `nx_number`,`at_number`, `nx_password`) VALUES ('%s','%s',%d, '13800138000', 1, '','+254711082439','');"%(s1,s1,b))