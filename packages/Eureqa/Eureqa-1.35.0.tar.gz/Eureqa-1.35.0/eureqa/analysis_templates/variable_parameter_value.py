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


from parameter_value import ParameterValue

import json

class VariableParameterValue(ParameterValue):
    """Variable parameter value for analysis template

    :var str id: The id of the parameter.
    :var str value: The parameter value.
    """

    def __init__(self, eureqa, id, value):
        """Initializes a new instance of the ~VariableParameter class
        :param str id: The id of the parameter.
        :param str value: The parameter value.
        """
        ParameterValue.__init__(self, id, value, 'variable')

    def _to_json(self):
        body = {}
        ParameterValue._to_json(self, body)
        return body

    def __str__(self):
        return json.dumps(self._to_json(), indent=4)

    @staticmethod
    def _from_json(eureqa, body):
        param = VariableParameterValue(None, None, None)
        ParameterValue._from_json(param, body)
        if param._type != "variable": raise Exception("Invalid type '%s' specified for variable parameter value" % param._type)
        return param
