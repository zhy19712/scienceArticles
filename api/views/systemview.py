from rest_framework.response import Response
from rest_framework.views import APIView
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from sougou_weixin.sougou_weixin import start_process
from sougou_weixin.util import tick


class StartWeinxinView(APIView):
    def get(self, request):
        scheduler = BlockingScheduler()
        scheduler.add_job(tick, 'interval', seconds=600)
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


