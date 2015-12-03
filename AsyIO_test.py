# -*- coding: utf-8 -*-_
__author__ = 'ZombieGroup'

from Requests import *
from Topic import Topic
from Question import Question
from DataBase import DataBase
from ReadData import ReadData
from gevent.pool import Group

user = 'root'
host = 'localhost'
password = ''
dbname = 'zhihu'
database = DataBase(user, host, password, dbname)
readdata = ReadData(user, host, password, dbname)
#result = Queue()
topic = Topic("http://www.zhihu.com/topic/19554927")


def question_slave(name):
    try:
        while True:
            question = question_queue.get_nowait()
            print 'slave %s get one question from the queue' % name
            database.put_question_in_db(question)
            question.get_answers()
    except Empty:
        print 'slave %s is dead' % name


def answer_slave(name):
    try:
        while True:
            answer = answer_queue.get_nowait()
            print 'slave %s get one answer from the queue' % name
            database.put_answer_in_db(answer)
            answer.get_upvoters()
    except Empty:
        print 'slave %s is dead' % name


def user_slave(name):
    try:
        while True:
            user = user_queue.get_nowait()
            print 'slave %s get one user from the queue' % name
            database.put_user_in_db(user)
    except Empty:
        print 'slave %s is dead' % name


def master(name):
    print 'master %s'%name
    topic.get_questions()

masters = [gevent.spawn(master, i) for i in xrange(10)]
users = [gevent.spawn(user_slave,i) for i in xrange(100)]
questions = [gevent.spawn(question_slave,i) for i in xrange(100)]
answers = [gevent.spawn(answer_slave,i) for i in xrange(100)]
gevent.joinall(masters+users+questions+answers)

