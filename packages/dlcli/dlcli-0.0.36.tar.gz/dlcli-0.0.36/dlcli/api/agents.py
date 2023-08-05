import logging
import requests
import utils

logger = logging.getLogger(__name__)


class Agents(object):
    def __init__(self, ctx):
        self.ctx = ctx
        self.headers = {'Authorization': "Bearer " + ctx.parent.parent.params['key']}

    def get_agents(self):
        return requests.get(
            utils.build_api_url(self.ctx, 'agents'),
            headers=self.headers).json()

    def register_agent(self, payload):
        return requests.post(
            utils.build_api_url(self.ctx, 'agents/register'),
            headers=self.headers,
            data=payload)

    def delete_agent(self, agent):
        return requests.delete(
            utils.build_api_url(self.ctx, 'agents') + '/' + agent,
            headers=self.headers)

    def get_agent_name_from_id(self, id):
        agents = requests.get(
            utils.build_api_url(self.ctx, 'agents'),
            headers=self.headers).json()
        for a in agents:
            if a['id'] == id:
                return a['name']
