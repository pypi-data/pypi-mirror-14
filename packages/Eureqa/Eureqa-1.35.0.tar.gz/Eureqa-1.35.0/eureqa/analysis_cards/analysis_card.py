# Copyright (c) 2016, Nutonian Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the Nutonian Inc nor the
#     names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL NUTONIAN INC BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


class AnalysisCard(object):
    """The base class for all card classes. API returns an instance of this class if it cannot recognize
    the type of the card that it receives from the server."""

    def __init__(self, body, eureqa):
        """For internal use only"""

        self._analysis_id = body['analysis_id']
        self._id = body['item_id']
        self._order = body['order_index']
        self._eureqa = eureqa
        self._body = body

    def delete(self):
        """Deletes the card from the server."""
        endpoint = '/analysis/%s/items/%s' % (self._analysis_id, self._id)
        self._eureqa._session.report_progress('Deleting card: \'%s\' from analysis: \'%s\'.' % (self._id, self._analysis_id))
        self._eureqa._session.execute(endpoint, 'DELETE')

    def _update_card(self):
        endpoint = '/analysis/%s/items/%s' % (self._analysis_id, self._id)
        self._eureqa._session.report_progress('Updating card: \'%s\' from analysis: \'%s\'.' % (self._id, self._analysis_id))
        new_body = self._eureqa._session.execute(endpoint, 'PUT', self._body)
        new_instance = self.__class__(new_body, self._eureqa)
        self.__dict__ = new_instance.__dict__

    def move_above(self, other_card):
        """Moves this card above another card.

        :param other_card: The other card object above which to move this card.
        """

        other_card_order = other_card._order if hasattr(other_card, '_order') else other_card
        if other_card_order >= self._order:
            return
        self._body['order_index'] = other_card_order
        self._update_card()

    def move_below(self, other_card):
        """Moves this card below another card.

        :param other_card: The other card object below which to move this card.
        """

        other_card_order = other_card._order if hasattr(other_card, '_order') else other_card
        if other_card_order <= self._order:
            return
        self._body['order_index'] = other_card_order
        self._update_card()
