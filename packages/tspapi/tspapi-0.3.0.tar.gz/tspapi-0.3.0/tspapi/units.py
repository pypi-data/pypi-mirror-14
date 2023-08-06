# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# -*- coding: utf-8 -*-

from requests.structures import LookupDict

_units = {

    # Informational.
    'bytecount': ('bytecount',),
    'duration': ('duration',),
    'number': ('number',),
    'percent': ('percent',),
}

units = LookupDict(name='units')

for code, titles in _units.items():
    for title in titles:
        setattr(units, title, code)
        if not title.startswith('\\'):
            setattr(units, title.upper(), code)
