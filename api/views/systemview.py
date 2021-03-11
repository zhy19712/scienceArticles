from rest_framework.response import Response
from rest_framework.views import APIView
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from sougou_weixin import run_weixin_crawler
from sougou_weixin.util import tick


class StartWeinxinView(APIView):
    def get(self, request):
        scheduler = BlockingScheduler()
        scheduler.add_job(run_weixin_crawler, 'interval', seconds=3)
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
        response = {
            'code': 1,
            'data': 'started!',
        }
        return Response(response)


