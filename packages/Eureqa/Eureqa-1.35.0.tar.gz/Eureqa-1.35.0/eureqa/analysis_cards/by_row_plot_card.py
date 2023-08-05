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

from analysis_card import AnalysisCard
import json

class ByRowPlotCard(AnalysisCard):
    """Represents a variable line graph on the server.

    :var str ~eureqa.analysis_cards.ByRowPlotCard.title: The card's title.
    :var str ~eureqa.analysis_cards.ByRowPlotCard.focus_variable: Focused (foreground) variable for the card.  Must be a member of ~eureqa.analysis_cards.ByRowPlotCard.plotted_variables
    :var str ~eureqa.analysis_cards.ByRowPlotCard.x_var: Name of the variable to plot as the X axis
    :var list ~eureqa.analysis_cards.ByRowPlotCard.plotted_variables: Variables to plot.  (List of string variable names.)
    :var bool ~eureqa.analysis_cards.ByRowPlotCard.should_center: Should the plot be centered?
    :var bool ~eureqa.analysis_cards.ByRowPlotCard.should_scale: Should the plot scale?
    """
        
    @property
    def focus_variable(self):
        """The variable that is currently in focus (in the foreground) for this card.
        Must be a member of 'plotted_variables'.

        :return: focus_variable for this card
        :rtype: str
        """
        
        return self._options['focusVariable']

    @focus_variable.setter
    def focus_variable(self, val):
        self._options['focusVariable'] = val
        self._update_card()

    @property
    def _options(self):
        return self._body['content']['options']

    @property
    def x_var(self):
        """The X-axis variable for this card

        :return: the name of the X-axis variable for this card
        :rtype: str
        """
        
        return self._options['xAxisVariable']

    @x_var.setter
    def x_var(self, val):
        self._options['xAxisVariable'] = val
        self._update_card()

    @property
    def plotted_variables(self):
        """The plotted variables for this card.

        :return: List of the names of the variables being plotted against the X axis
        :rtype: tuple
        """
        
        ## Return a tuple because we don't currently support adding or removing variables
        return self._options['plottedVariables']

    @plotted_variables.setter
    def plotted_variables(self, val):
        self._options['plottedVariables'] = val
        self._update_card()
    
    @property
    def should_center(self):
        """The should_center option for this card.

        :return: whether this plot should be centered
        :rtype: bool
        """
        
        return self._options['shouldCenter']

    @should_center.setter
    def should_center(self, val):
        self._options['shouldCenter'] = val
        self._update_card()

    @property
    def should_scale(self):
        """The should_scale option for this card.

        :return: whether this plot should be scaled
        :rtype: bool
        """
        
        return self._options['shouldScale']

    @should_scale.setter
    def should_scale(self, val):
        self._options['shouldScale'] = val
        self._update_card()
        
    @property
    def title(self):
        """The title of this card.

        :return: title of this card
        :rtype: str"""
        
        return self._body['content']['title']

    @title.setter
    def title(self, value):
        self._body['content']['title'] = value
        self._update_card()

    @property
    def description(self):
        """ The description of this card.

        :return: description of this card
        :rtype: str"""
        return self._body['content']['description']

    @description.setter
    def description(self, value):
        self._body['content']['description'] = value
        self._update_card()
    
    @property
    def collapse(self):
        """Whether the card is collapsed by default.

        :return: whether the card is collapsed by default
        :rtype: str"""
        return self._body['collapse']

    @collapse.setter
    def collapse(self, value):
        self._body['collapse'] = value
        self._update_card()
