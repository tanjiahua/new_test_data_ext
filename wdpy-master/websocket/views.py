# !/usr/local/python/bin/python3
import os
import traceback

from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import paramiko

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.dirname(os.path.dirname(path))


@accept_websocket
def faker_data_nga_truemoni(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            print(traceback.print_exc())
            return render(request, 'index_nga_truemoni.html')
    else:
        try:
            for message in request.websocket:
                message = message.decode('utf-8')  # 接收前端发来的数据
                print(message)
                if message == 'backup_all_pre30':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_truemoni/pre_order_status_30.py'% path
                elif message == 'backup_all_pre40':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_truemoni/pre_order_status_40.py'% path
                elif message == 'backup_all_bind':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_truemoni/bind_card_wait_apply.py'% path
                elif message == 'backup_apply_reduction':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_truemoni/apply_reduction_749.py'% path
                elif message == 'backup_all_20':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_truemoni/order_status_20.py'% path
                elif message == 'backup_all':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_truemoni/order_status_30.py'% path
                elif message == 'backup_all_32':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_truemoni/order_status_32.py'% path
                elif message == 'backup_all_36':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_truemoni/order_status_36.py'% path
                elif message == 'backup_all_1':
                    command = 'python3 %s/y1_nga_test_data_truemoni/order_status_40.py'% path
                elif message == 'backup_all_60':
                    command = 'python3 %s/y1_nga_test_data_truemoni/order_status_60.py'% path
                elif message == 'backup_all_99':
                    command = 'python3 %s/y1_nga_test_data_truemoni/order_status_99.py'% path
                elif message == 'backup_all_d0':
                    command = 'python3 %s/y1_nga_test_data_truemoni/d0_exceeding_order.py'% path
                elif message == 'backup_all_d1':
                    command = 'python3 %s/y1_nga_test_data_truemoni/d1_exceeding_order.py'% path
                else:
                    request.websocket.send('请申请权限!!!'.encode('utf-8'))
                # 远程连接服务器
                hostname = '172.20.240.192'
                username = 'root'
                password = 'tYy191vzrftwglXJ'
                #hostname = '127.0.0.1'
                #username = 'liwenli'
                #password = 'liwenli'
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname,username=username, password=password)
                # 务必要加上get_pty=True,否则执行命令会没有权限
                stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
                # result = stdout.read()
                # 循环发送消息给前端页面
                while True:
                    nextline = stdout.readline().strip()  # 读取脚本输出内容
                    print(nextline.strip())
                    request.websocket.send(nextline.encode('utf-8')) # 发送消息到客户端
                    # 判断消息为空时,退出循环
                    if not nextline:
                        break
                ssh.close()  # 关闭ssh连接

        except Exception:
            print(traceback.print_exc())

@accept_websocket
def faker_data_nga_nairaforever(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            print(traceback.print_exc())
            return render(request, 'index_nga_nairaforever.html')
    else:
        try:
            for message in request.websocket:
                message = message.decode('utf-8')  # 接收前端发来的数据
                print(message)
                if message == 'backup_all_pre30':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_nairaforever/pre_order_status_30.py'% path
                elif message == 'backup_all_pre40':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_nairaforever/pre_order_status_40.py'% path
                elif message == 'backup_all_bind':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_nairaforever/bind_card_wait_apply.py'% path
                elif message == 'backup_apply_reduction':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_nairaforever/apply_reduction_749.py'% path
                elif message == 'backup_all':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_nairaforever/order_status_30.py'% path
                elif message == 'backup_all_32':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_nairaforever/order_status_32.py'% path
                elif message == 'backup_all_36':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_nairaforever/order_status_36.py'% path
                elif message == 'backup_all_1':
                    command = 'python3 %s/y1_nga_test_data_nairaforever/order_status_40.py'% path
                elif message == 'backup_all_60':
                    command = 'python3 %s/y1_nga_test_data_nairaforever/order_status_60.py'% path
                elif message == 'backup_all_99':
                    command = 'python3 %s/y1_nga_test_data_nairaforever/order_status_99.py'% path
                elif message == 'backup_all_d0':
                    command = 'python3 %s/y1_nga_test_data_nairaforever/d0_exceeding_order.py'% path
                elif message == 'backup_all_d1':
                    command = 'python3 %s/y1_nga_test_data_nairaforever/d1_exceeding_order.py'% path
                else:
                    request.websocket.send('请申请权限!!!'.encode('utf-8'))
                # 远程连接服务器
                hostname = '172.20.240.192'
                username = 'root'
                password = 'tYy191vzrftwglXJ'
                #hostname = '127.0.0.1'
                #username = 'liwenli'
                #password = 'liwenli'
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname,username=username, password=password)
                # 务必要加上get_pty=True,否则执行命令会没有权限
                stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
                # result = stdout.read()
                # 循环发送消息给前端页面
                while True:
                    nextline = stdout.readline().strip()  # 读取脚本输出内容
                    print(nextline.strip())
                    request.websocket.send(nextline.encode('utf-8')) # 发送消息到客户端
                    # 判断消息为空时,退出循环
                    if not nextline:
                        break
                ssh.close()  # 关闭ssh连接

        except Exception:
            print(traceback.print_exc())

@accept_websocket
def faker_data_nga_aceloan(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            print(traceback.print_exc())
            return render(request, 'index.html')
    else:
        try:
            for message in request.websocket:
                message = message.decode('utf-8')  # 接收前端发来的数据
                print(message)
                if message == 'backup_all_pre30':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_aceloan/pre_order_status_30.py'% path
                elif message == 'backup_all_pre40':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_aceloan/pre_order_status_40.py'% path
                elif message == 'backup_all_bind':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_aceloan/bind_card_wait_apply.py'% path
                elif message == 'backup_apply_reduction':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_aceloan/apply_reduction_749.py'% path
                elif message == 'backup_all':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_aceloan/order_status_30.py'% path
                elif message == 'backup_all_32':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_aceloan/order_status_32.py'% path
                elif message == 'backup_all_36':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_aceloan/order_status_36.py'% path
                elif message == 'backup_all_1':
                    command = 'python3 %s/y1_nga_test_data_aceloan/order_status_40.py'% path
                elif message == 'backup_all_60':
                    command = 'python3 %s/y1_nga_test_data_aceloan/order_status_60.py'% path
                elif message == 'backup_all_99':
                    command = 'python3 %s/y1_nga_test_data_aceloan/order_status_99.py'% path
                elif message == 'backup_all_d0':
                    command = 'python3 %s/y1_nga_test_data_aceloan/d0_exceeding_order.py'% path
                elif message == 'backup_all_d1':
                    command = 'python3 %s/y1_nga_test_data_aceloan/d1_exceeding_order.py'% path
                else:
                    request.websocket.send('请申请权限!!!'.encode('utf-8'))
                # 远程连接服务器
                hostname = '172.20.240.192'
                username = 'root'
                password = 'tYy191vzrftwglXJ'
                #hostname = '127.0.0.1'
                #username = 'liwenli'
                #password = 'liwenli'
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname,username=username, password=password)
                # 务必要加上get_pty=True,否则执行命令会没有权限
                stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
                # result = stdout.read()
                # 循环发送消息给前端页面
                while True:
                    nextline = stdout.readline().strip()  # 读取脚本输出内容
                    print(nextline.strip())
                    request.websocket.send(nextline.encode('utf-8')) # 发送消息到客户端
                    # 判断消息为空时,退出循环
                    if not nextline:
                        break
                ssh.close()  # 关闭ssh连接

        except Exception:
            print(traceback.print_exc())


@accept_websocket
def faker_data_nga_moneyaccess(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            print(traceback.print_exc())
            return render(request, 'index_nga_moneyaccess.html')
    else:
        try:
            for message in request.websocket:
                message = message.decode('utf-8')  # 接收前端发来的数据
                print(message)
                if message == 'backup_all_pre30':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_moneyaccess/pre_order_status_30.py'% path
                elif message == 'backup_all_pre40':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_moneyaccess/pre_order_status_40.py'% path
                elif message == 'backup_all_bind':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_moneyaccess/bind_card_wait_apply.py'% path
                elif message == 'backup_apply_reduction':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_moneyaccess/apply_reduction_749.py'% path
                elif message == 'backup_all':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_moneyaccess/order_status_30.py'% path
                elif message == 'backup_all_32':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_moneyaccess/order_status_32.py'% path
                elif message == 'backup_all_36':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_moneyaccess/order_status_36.py'% path
                elif message == 'backup_all_1':
                    command = 'python3 %s/y1_nga_test_data_moneyaccess/order_status_40.py'% path
                elif message == 'backup_all_60':
                    command = 'python3 %s/y1_nga_test_data_moneyaccess/order_status_60.py'% path
                elif message == 'backup_all_99':
                    command = 'python3 %s/y1_nga_test_data_moneyaccess/order_status_99.py'% path
                elif message == 'backup_all_d0':
                    command = 'python3 %s/y1_nga_test_data_moneyaccess/d0_exceeding_order.py'% path
                elif message == 'backup_all_d1':
                    command = 'python3 %s/y1_nga_test_data_moneyaccess/d1_exceeding_order.py'% path
                else:
                    request.websocket.send('请申请权限!!!'.encode('utf-8'))
                # 远程连接服务器
                hostname = '172.20.240.192'
                username = 'root'
                password = 'tYy191vzrftwglXJ'
                #hostname = '127.0.0.1'
                #username = 'liwenli'
                #password = 'liwenli'
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname,username=username, password=password)
                # 务必要加上get_pty=True,否则执行命令会没有权限
                stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
                # result = stdout.read()
                # 循环发送消息给前端页面
                while True:
                    nextline = stdout.readline().strip()  # 读取脚本输出内容
                    print(nextline.strip())
                    request.websocket.send(nextline.encode('utf-8')) # 发送消息到客户端
                    # 判断消息为空时,退出循环
                    if not nextline:
                        break
                ssh.close()  # 关闭ssh连接

        except Exception:
            print(traceback.print_exc())

@accept_websocket
def faker_data_nga_ngmoni(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            print(traceback.print_exc())
            return render(request, 'index_ng_ngmoni.html')
    else:
        try:
            for message in request.websocket:
                message = message.decode('utf-8')  # 接收前端发来的数据
                print(message)
                if message == 'backup_all_pre30':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_ngmoni/pre_order_status_30.py'% path
                elif message == 'backup_all_pre40':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_ngmoni/pre_order_status_40.py'% path
                elif message == 'backup_all_bind':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_ngmoni/bind_card_wait_apply.py'% path
                elif message == 'backup_apply_reduction':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_ngmoni/apply_reduction_749.py'% path
                elif message == 'backup_all':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_ngmoni/order_status_30.py'% path
                elif message == 'backup_all_32':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_ngmoni/order_status_32.py'% path
                elif message == 'backup_all_36':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_ngmoni/order_status_36.py'% path
                elif message == 'backup_all_1':
                    command = 'python3 %s/y1_nga_test_data_ngmoni/order_status_40.py'% path
                elif message == 'backup_all_60':
                    command = 'python3 %s/y1_nga_test_data_ngmoni/order_status_60.py'% path
                elif message == 'backup_all_99':
                    command = 'python3 %s/y1_nga_test_data_ngmoni/order_status_99.py'% path
                elif message == 'backup_all_d0':
                    command = 'python3 %s/y1_nga_test_data_ngmoni/d0_exceeding_order.py'% path
                elif message == 'backup_all_d1':
                    command = 'python3 %s/y1_nga_test_data_ngmoni/d1_exceeding_order.py'% path
                else:
                    request.websocket.send('请申请权限!!!'.encode('utf-8'))
                # 远程连接服务器
                hostname = '172.20.240.192'
                username = 'root'
                password = 'tYy191vzrftwglXJ'
                #hostname = '127.0.0.1'
                #username = 'liwenli'
                #password = 'liwenli'
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname,username=username, password=password)
                # 务必要加上get_pty=True,否则执行命令会没有权限
                stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
                # result = stdout.read()
                # 循环发送消息给前端页面
                while True:
                    nextline = stdout.readline().strip()  # 读取脚本输出内容
                    print(nextline.strip())
                    request.websocket.send(nextline.encode('utf-8')) # 发送消息到客户端
                    # 判断消息为空时,退出循环
                    if not nextline:
                        break
                ssh.close()  # 关闭ssh连接

        except Exception:
            print(traceback.print_exc())

@accept_websocket
def faker_data_ke_kencash(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            print(traceback.print_exc())
            return render(request, 'index_ke_kencash.html')
    else:
        try:
            for message in request.websocket:
                message = message.decode('utf-8')  # 接收前端发来的数据
                print(message)
                if message == 'backup_all_pre30':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_ke_test_data_kencash/pre_order_status_30.py'% path
                elif message == 'backup_all_pre40':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_ke_test_data_kencash/pre_order_status_40.py'% path
                elif message == 'backup_all_bind':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_aceloan/bind_card_wait_apply.py'% path
                elif message == 'backup_apply_reduction':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_nga_test_data_aceloan/apply_reduction_749.py'% path
                elif message == 'backup_all':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_ke_test_data_kencash/order_status_30.py'% path
                elif message == 'backup_all_32':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_ke_test_data_kencash/order_status_32.py'% path
                elif message == 'backup_all_36':#这里根据web页面获取的值进行对应的操作
                    command = 'python3 %s/y1_ke_test_data_kencash/order_status_36.py'% path
                elif message == 'backup_all_1':
                    command = 'python3 %s/y1_ke_test_data_kencash/order_status_40.py'% path
                elif message == 'backup_all_60':
                    command = 'python3 %s/y1_ke_test_data_kencash/order_status_60.py'% path
                elif message == 'backup_all_99':
                    command = 'python3 %s/y1_ke_test_data_kencash/order_status_99.py'% path
                elif message == 'backup_all_d0':
                    command = 'python3 %s/y1_ke_test_data_kencash/d0_exceeding_order.py'% path
                elif message == 'backup_all_d1':
                    command = 'python3 %s/y1_ke_test_data_kencash/d1_exceeding_order.py'% path
                else:
                    request.websocket.send('请申请权限!!!'.encode('utf-8'))
                # 远程连接服务器
                hostname = '172.20.240.192'
                username = 'root'
                password = 'tYy191vzrftwglXJ'
                #hostname = '127.0.0.1'
                #username = 'liwenli'
                #password = 'liwenli'
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname,username=username, password=password)
                # 务必要加上get_pty=True,否则执行命令会没有权限
                stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
                # result = stdout.read()
                # 循环发送消息给前端页面
                while True:
                    nextline = stdout.readline().strip()  # 读取脚本输出内容
                    print(nextline.strip())
                    request.websocket.send(nextline.encode('utf-8')) # 发送消息到客户端
                    # 判断消息为空时,退出循环
                    if not nextline:
                        break
                ssh.close()  # 关闭ssh连接

        except Exception:
            print(traceback.print_exc())
