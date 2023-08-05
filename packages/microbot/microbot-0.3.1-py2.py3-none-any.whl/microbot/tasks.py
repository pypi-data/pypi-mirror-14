from __future__ import absolute_import
from celery import shared_task
from microbot.models import Update, Bot
import logging

logger = logging.getLogger(__name__)

@shared_task
def handle_message(update_id, bot_id):
    try:
        update = Update.objects.get(id=update_id)
    except Update.DoesNotExist:
        
        return "Error: order %s does not exists" % order_number
    else:
        if not force and order.order_file:
            return "Order %s already generated" % order_number
        try:
            exporter = Exporter()
            filename = exporter.export(order)
            f = open(filename)
            order.order_file.save(filename,File(f))
            return "Order %s file generated" % filename
        except:
            return "Unexpected error: Order %s not generated: %s" % (order_number, sys.exc_info()[0]) 