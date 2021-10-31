from Helper.MyHelper import MyHelper
from datetime import datetime
import sched, time

s = sched.scheduler(time.time, time.sleep)
job = MyHelper()
job.do()
