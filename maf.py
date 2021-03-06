#!/usr/bin/env python
# coding: ISO8859-1
#
# Copyright (c) 2013, Preferred Infrastructure, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
maf - a waf extension for automation of parameterized computational experiments
"""

# NOTE: coding ISO8859-1 is necessary for attaching maflib at the end of this
# file.

import os
import os.path
import shutil
import subprocess
import sys
import tarfile
import waflib.Context
import waflib.Logs

TAR_NAME = 'maflib.tar'
NEW_LINE = '#XXX'.encode()
CARRIAGE_RETURN = '#YYY'.encode()
ARCHIVE_BEGIN = '#==>\n'.encode()
ARCHIVE_END = '#<==\n'.encode()

class _Cleaner:
    def __init__(self, directory):
        self._cwd = os.getcwd()
        self._directory = directory

    def __enter__(self):
        self.clean()

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self._cwd)
        if exc_type:
            self.clean()
        return False

    def clean(self):
        try:
            path = os.path.join(self._directory, 'maflib')
            shutil.rmtree(path)
        except OSError:
            pass

def _read_archive(filename):
    if filename.endswith('.pyc'):
        filename = filename[:-1]

    with open(filename, 'rb') as f:
        while True:
            line = f.readline()
            if not line:
                raise Exception('archive not found')
            if line == ARCHIVE_BEGIN:
                content = f.readline()
                if not content or f.readline() != ARCHIVE_END:
                    raise Exception('corrupt archive')
                break

    return content[1:-1].replace(NEW_LINE, '\n'.encode()).replace(
        CARRIAGE_RETURN, '\r'.encode())

def unpack_maflib(directory):
    with _Cleaner(directory) as c:
        content = _read_archive(__file__)

        os.makedirs(os.path.join(directory, 'maflib'))
        os.chdir(directory)

        bz2_name = TAR_NAME + '.bz2'
        with open(bz2_name, 'wb') as f:
            f.write(content)

        try:
            t = tarfile.open(bz2_name)
        except:
            try:
                os.system('bunzip2 ' + bz2_name)
                t = tarfile.open(TAR_NAME)
            except:
                raise Exception('Cannot extract maflib. Check that python bz2 module or bunzip2 command is available.')

        try:
            t.extractall()
        finally:
            t.close()

        try:
            os.remove(bz2_name)
            os.remove(TAR_NAME)
        except:
            pass

        maflib_path = os.path.abspath(os.getcwd())
        return maflib_path

def test_maflib(directory):
    try:
        os.stat(os.path.join(directory, 'maflib'))
        return os.path.abspath(directory)
    except OSError:
        return None

def find_maflib():
    path = waflib.Context.waf_dir
    if not test_maflib(path):
        unpack_maflib(path)
    return path

find_maflib()
import maflib.core
#==>
#BZh91AY&SY��n� o�����]N������������ @( �`k�z�݇�{�'��k}���w��t�p=��B��*�:�$�-�/���M�;�t�$2��}>����}���7h�<��)��݃v � Q������˷�����=�w��m%vӯ>��l{�E@Ƕ�;��u6���;bH^�޼����1���ǼM��C�r�y\{(8�8��2��h�6.��gWun����*Q�3�[2��lζ>����� u�t�:��"T�ֽo@N�WIگ�;f��)!�q��ݣ>���ۻ��P4� &@�14�S�LS�i��h`� =M #YYY d"F�� �e2�=CF�    hdA"d4�Bz6��S@�@� #XXXHA4'�50#@j�)�=�2z�����=2�   4"H�#YYYL���BbaOF�l4I�d�ɢ4mSM�����h��Py���FBhh��4��)��5?T�#YYY��P = 4h�#YYY�����>���� DBf'��J/_���l��C؛V!��.NXa1�5�vEZ$��T@��&E	$��_���>���ھ�f��~��C�̟�w��L?�>'������`6����4b��~��X���(i���X�H>7�B'hE�(J#��vP'E��ĭ^�������R�WNU`�#YYY�wTD~dX�*)�TM��x2�)N��4��#�����,�M�'���p�LSZb#	��%(؉��-�DKr!�V�\�Q � �f�����p�I��h��^`&�v�	���໣�5���"�����%�ΐ���fѧ�M4ms�F(���T@�#XXX<�)�>��k_�(p��g���V�`\��G��� y�'�u���1�5�7�B��=���K'%�����R�f��� )s���q�*։>欽<.����w�zz���d.��Gc�g1iG,0Ȃcх�:��(ؘ��X����(Z�5vN[d�ny�={!�)d୭p#XXXuڛ�������j��A�=�m��~cE�+���'r�2+��z�߆�!��\���Ag��M%�]JYv�i��H�o��k��F��O~���m]=4�ކ|�6��/:ޫ���\aQM�:9��e��,�3���kd��.��ƻ�e��@��R3i ��~��d���e��(t'#��R�H"��'�	���`�����CG��J�	�vc��v��.���T>3?�r7�8����� O:1��Kz��K�d�] [��D�`7T��:����#u�>�~���4'�#XXXw�Q!bV���;��Mr�~�U>,�0�+�BPZ�#�n���>�Y$����C�n3'nKC��.�������=������>E�;#YYY#����QX�M4xd�ᦠIXx���4��9w�.g�#XXXT4�������hǶ<k�`�z�����g��ArD�M���ހ�G},,?�9F��~Ӭ���a�S��6�PI����p|�������p���8D�~5� �mô���#��Oy������� ��@@]�T�$I;���`�C&ZV�����ǫ��݀3�M��՘�zM.�{Tf;�ABA$2<{wy#YYY[y�n煨9B��M@���U/@3����:�B#XXX������� �O��ob�cf�`�_P���b�%ۗ��g:���=�7������<��o�!����	 ��#H9�����Hxs��z��mC�_��:�jx��-HY_9��c�ٖl} �Fs#XXX���U��\����� �#y�%��#��i�&ޗ�9���}C��o��V���D�����G��ͳ�j�6��܆�2Ǻ�a��F���W���n�����zq��h�O��<O��nr� �Vm�^�h��Ia	�g�x��%����q�w{�బ�jGtp����vðI	�>�w� �j�|r��m�>�-�,8��M]_Hv�y~��> ���ҟ�j;|w�n��[�/�����i��ݰ�6?8���7��t�<�?q�#��8�]�l>E6��3���귻�f���J۷��:��˔���i�9lm���7�#YYYǜ���N��[*yk[6���z������3�a��T, ��N0��k��Ơl�ӈ��{�:z��Z����ۅ��pv�P@�`\d�zI�����6����r��zͧ � ��cD���ǎ@�H`@&�U�<NCA��o1���\�0l=G��M�(�r<;y�W.�m�kóM:��|�"�q��t���>� ��9���B�%����Gx�b^���9C0�J<��8��k��uh��=Nh#�/o�@�������x�f�T�0�q��b���'<�QB��<�5I�O���s���GW)�45��L#YYY&E��4�&��nN622#YYY�1�~WN1��zӖ��A�Y`Kt��H����Q�%��&	�G�E���t�oo1y�>m�;����H�ȾC�ڽ��,�� ߞ�,�2W,yu�y/_,�ygǃF3�O��T�?L&����F4�ni�qF'b ��`�;�^�0�.�dw�Ɇ��ďC�a�HLJ��q$'@�Z����+rӰ��p7ƣ�8c�Tk��j��o�G%�1� �H.7�������3��S�G[�H�	l��!\Ed�u�0(x�68���n� ���u�D4�vΣ����$4e����G�̥� �}�xBe��+� ���+�X�@S���F.q������>�w��;����`�������ɓ�=�s�nM�8=�­�=��sGm���o��a!�i��9՝y��o<�%��֙B�,T�x�J�ů�	�� �R���M��9mU.6�-1(I���k�� ���U�.�]s���b��a���o#YYY]sQ+�">�i��]N�F|�!Ar�7O����ؠ�^���wD�^&�Ĕ\��d�L��i!D�=�HwoN@�%�WV�㴗����E�a�Ʈ���B�$ur������i�!�	�V�?=@�,5 ���L�z���,���d̏�j�����Y��Z��ć,!̇jA?�h�TP0j�#XXX7 �'���d�ĲsQk�ב앍T��gK���g��Ddo���ԕ�Z�l�uD��A�$�M��:�,��=V#VhD�u�kc��Y��9�����M�� ��!��dϰ3p�ͮļA�I��X��(Pq���Z�����;�d�U�H�ǰ�Ȗ�s����.=��$:��J�%x����DxÜ�<��v��E�5BB�G>��~e�g�KTJ��>�@YϘ1���y��=�B��h#��f����c�����י��6U�h<:�1xo�$8ZL�e�l���}F0�;���(;�#�85������������,�[���UTM�Ww���y�&���d�,K�^�K[;���ج�����܉�\;h��r�&�(8�z�d �t��2���n���]"\v�j;���j;���#��~�Wf��8|���P����S�Q�`�MRP;�5Z�yy�M�ς��#YYYE�a��"8���nn�W,��Nq�Pxx��#��L�k2k���&�bl�.MdlV�M��Q =���u�^���Ü#YYY�$�yN�@ΌT�8^�$���';Z4�p��� ?V\���C�H�Qmw�,*�Q�(�K�.F�<����%�#"NAM܍%��7�p#"�!�!�Ah�T�x?��(.��3�Έ���#XXXh�QŉHJ FP��Uu��w�/M�}Iԅt��p��o'o��*4A!�#XXX \a#YYYم@~+B��1>gYE2 �R��r��m�@?&/�Z��y�p�����֡�]`{�T�-$:��! j�f�DJt��vj�e>�r��O&��^�d�U��~XY��$d枓����~�a:��0�&{�cgC\�^@툠��qr��0n�M�B3M0 ��u죰v� ����!��#�1�����?l��x�GC+�%�xHj3�ߪ�x�m�;�u�-�< Ʀć80�6s��P+�e�$�{��㵘O	��0\$�͜���յ�2h@��[���r� �J��N`DU�����R�DV�b��o�D������W�5�D���n�	��r�d.- �&j�;�#YYY�j����I2��L판O���*�˞ٖ-4x�LV������UH���#C�ɾݧ��j��S�9�vǟ���ff�����%|���NB`ç�'q	����B8��#XXX�9��s��Ge�������d>"���<b&@�h�y��7�[Chd�g�xc5�ϓ��F��M +��X�(Y�KƝ#YYY�H[�U- 0��#9Y�H�S��a�A��:r��sv�:u@�U�vvR��X:h0��]T�|ܾi	��r���p�����.J���N	뿏��k�.�!k��n&���?V�D"���<j�:���簴\ʆ�&_�&�҃-惹���{,EN_��Y���$C�����\m�{t�6[�^T_��: )�o�p�����a�﵉3��q[t#XXX��ŏ�ꭾ�;Ї3�h�l�o���&`]W�H����/95ۚ8DnmL�Ԡ�p�-���bC���OȾ~�F4��K��8kv��O���r*��W�9����]d��x�T���G���%M1���X��mu$XF</��"[��=:$Y�"L'et#�\���Qk,�Ǵ���v._A�- _}�z.bZM��#XXX'8����W��1@����x�JQ@�{9� ��*�1���#B}`�(A���w����dy7 �*t�����@f�޻��o�bsr�r�܊��xs�3��"�Ρ�U��)1�#YYY����x�"<�O�$�OD Up��i'M�-�N���q�#XXX�����ݠ���4�'���踸��$�I���#YYYf͔�&�k^�W���S�M%?`#YYY���<������w�����vu�ŐQ���׎?��/Ӡ�Th���bj*Fh�c3Tr�*�y������g���B>xp�������z�l��������uR�Atu�D��&Sf��X=�4b�O',^�J[J���sTl#�7>#YYY|��������N�#XXX16�R1������I$#z�!������&3t?����0gǈG��|7��?�������FZ:!G��{�b��������^�"�3�����o�����q���"G��'HַO�g�u�sw������v���}��l�����w��x�EET��1�7ߋ�'7RHyE4׆�Y�!���~n5G���a�K2I���,0�����̸�i��_��Z>��_�����k�#XXX�1�=��9}&تd��C;�NM9ʡw�a�d^&g�ϧ���-����_�{o���B�� ��֭�dq#YYY��BQ0��g��|P;��]��_�i���Ch�����3��W��.��w�	����oԎ҆?8w�#�'����0�Թ.��e~p�#YYYK�#XXX>*���1�,FA��� t��"�R�AMi���`bd�V���#YYY���;y��\;0�j:x]A�G��,����G͏.{��d��2��.x�����{��`]�"��Bk�����"��&�h�vCXs����X}�Ϛ�y��/��K+�zʅ-.Qu�r&�Z���#Je�4�w�L�8�>�[2:&@���"�N�G�٣��"����vZŅ�D;7�ǟ�ͅ>1֝|�e�0���r�G��_IMe��)��Z؊ߨ"|+Ü̎1�9}>|kF�*����u<Z���-9m�al`�<�-������q�a���[�++YƟt5��x��u×�Ʊ���*��Ύ�G�p���7x!��PUk��׼�aVah����(՗NN��}�,􉱓�҆�|($�} �iʥ�����+��-hx<n]�[*?n����PsH.'/���Y����!�q��xz�|0,qb!<8;��"�#YYY�k�5P��#YYY�x�iy��Ƕ�����b8��8|@}���3���G�#XXX6�����\�H�Q���r3�(I�/��t����En��������%���>�^L� DA4�׮����]p�Y�{�8�Q9��O�7�rvT�o"��! r��/�`G*+�}˕��;���o�����҂ �/��>�!HT��Iz_��@؄^ˈ���'�o������С�j������k�{��#YYY'����1J��ڌz�y3�!#YYYJ>Y���>|U�Q����`��� ����K&e�&��_<��X��Otk����a����ư�3��?\�p;��˗4�sy�7a�����=>�94�PCp@o�3#YYY�����w�7���W��<�|⪪��zƖ�#YYY�25�>��� ?x3�|�ϑ��wo?�?�S��a�6����V�,���=vE t=@���@F�3�\A�|j���՚R�����⯫�'ݑ^5�j��]*逸���%��Kt���?�c�x�\V��h��� �$�H��q:u߫��)��rܶ�"��Q�ȍ��NDf�Y*����=_,�=� 5j8/zA�Ѹd!����)�t�x��e*K\�ƅ2+��t0�OQf�-�\�y�.	-�X�#}e�:7JBZ�g�zϞ �":���e��h6��i'���>	CO��2~��T�I�^�Y�Ϧh�)�x��[u�^gRB�	�5�G�|i �;ׁx?��<�m!����i6m��"��ԫo���W�iZR7��G�����N_*�C���]�?[���/%��w��(O�����U�U��� =GT�]��lL�f�g�G���s�Ӱ*0�(#XXX �s��u��@�(%_�^^��َ�҄�O\�J�4���rq{�h�^���ϛ�_��m���4�6�1�'�#XXXh��w�}��k�C�b<=���#���y�܇}s�ߛ��o�Ú�����M$!� .g�*g��拤tT�{�ga��(S�NR8bcyxqD��$kT߀2(c���u� \H �#XXXI �w��N�8��rM&��u-��B��a�;˥��[&>��"j��b>A�oF���]vb7�����]�{I�#��#k���V�2 �ċ WU����u�(7��2y���@J9�� %Pn�N��J�a�\1h$��s���^���vײ�( ��l�*t�#YYY�t�U�3|s��Q�#��]����_kh��}mv��f����7�4	���"��g�E}S�]�AT�x#"_�j����W�>�z���u� �_u����T>�~� ~�3����L�:-�,n�B-x7�>����	���߆�cǴ�����u��\�8��[��nw�<8��������8�~��/8D��Z��6�:�i���n�&�sE��������L��=�ȉ,,�@W��k�MK��fY��&_|Vtf�9��z���B�ToU��Y3��$�:"��C�b�-1�e����q��uz��[��EA�%}�P��vD�%0��<H �<���%�Z?:���K)�����q	]u���y����^T<��g���������0�r�&�T�%�}� ���m�D$!hD�#YYY�뉦�G�CD�7_�W��7$�p���RC�tx�����P�$�Q,�Q2�C��{�WV�u��+�o��e1}{n�\ꃵ�P���Ay�Riz�ǟ���\v';���{����#YYY��}�?��P�3D?9�d�jD��H& ��*����L�tto����^�>H��#XXXHBD�#XXX�B!� ��ISR�jZV�0��6�61hm`'�6��A��!C�<��>��i��庴���_Y¿ǘ�]�[�}����NP$������ňF��3�V1���O��x�j���``�0#XXX(�G��#YYY��߽���v^x���H�����Kc�giI��%�wn�ɬS�M�N����P[l0�������?�ϢxW�#XXX\��OϷϚ#XXXC荟�V�,p\���Иg�v���`���&��������'y�?���G����502}Ưq���)����1��S��t�9�56���C��F��,Ow������x�/Kl�����<�eHc�O��O�B=8pY����޶#YYY�P@��`,lnG�,Hz�:��G�u��h~u�{؞V|��x�����x�jOX���M#YYY��>��)��SA��������OF��'��y���)���r>�7�w�Y'e���|əߋV��ZJ���>��=��n���`z�y�q+��:/�<����o00Q��5�׍��;#XXXo)�l~�l��8�6��I���6��S ��a<(?w�۾���2��̧lu��؝B�MA�C�=�Cv��zL#YYYL�I��Ϡ��F�����f��>�p�W����>�d�%'���{pu+�Z�S�4_�����ji�8(��qFO��Ԟ#��l'�F��И06�Q�q��'?��NY�c�bR���8#XXX0o2`{�����u�(���n442?�JnJS_�hK}+�p�ߪb�v���zǸ�9������jlw��402q(�#YYY��:o6SQ�4t�U����a�Ͼ�i�v��3��lELD�{s%�-�q��cZ����}����	�O�Sk�Q��eI�09�=d�l>^᷶�R�#YYY�iSp�z��#`\���@3���	'g�ӏw��!#XXXȷ?�|P'�}\�����߫�J������)�9�x;����Hm���/}�~,lZXa�?�� W �1#�Ă�:Ģ$�����;�k%�:1n��͍7�~�%�F\ZCm{q�o������l��=�B�U����?J���c���28Mb��{q�h{���q���@�p$�Q`i>����$U��� T(�1�a�����J���~�:Hu8r�#*a"�F$$F�3?Y�p��[���s+����Y��M	��rs�eQâA��H^a	���Y(�%9��DwN�$8�!�L`J\X��qa�h��O�a?��7��%C��<4��<F|\�5&�哈ؓ�g��~��%~?�mws�=��hܖqJt4q�G�%�B���x��G�;��$���T�I�2�����ؘ��|4i��p�#�g�t`�:��oops%��;ٍv]�e�����G<Ձ�i��[c��ڠ~G��w�#*n�E;�Ž��ih:�f�Nw"�a�Ly�YwU���Ћ��^����M�ڊ�,��a�Za�?dL��nxBA�^����徰���)�D�Ih5/a[���v=���c*B[�#YYY�����մ��c<���,QPLOP�*h-ڛYV�q�U�z����4���7ǹz�zGP�(D�65)�3�Ke$6nF��0�N� �r�#p�b��P<��W#XXX����<�/6ғ{&�U���Q�����=����5r�{}���j����F����t������(�vC�5PHI4H��Hf�!7C�M������MR���i��T�;)�(�P=�}�ơr�+�1oVO�]A	�#XXX辎����_�P�����(3!��F)i����ad��2�R������CG����8x#^bP��˾#XXXR�Bԡ��$#XXXL.����_&��$d#0T<�_��#[��fe�݄F��@l��&uDj@c��h q{ۓ�����c�lA��/�G�y���aiC#�H�}�<(��q�Z*�����P�UG���M���L���kUT Jq7�M���Q����t��j��v��{n��J���s����>�fGf�[a5~ӷ�]�E��Y%@nE����j��n�T����ŻlbK%��#�C�d�%*�N�x�R��hp����dU&<�/r�yn�0�c��+Jð(�ē4@C/#�󘯈2I	E��{6��mX�#XXX���H�w\��y��7&���d2#YYY��)�u:�'p����E����@>8ZT�� !V%R` j�l,�N��n�V�|j�}���R�Ї��5;rv�Q*t#XXX�)L�UN븲0�'���FI��)_�'�M]�,�\�Û��J��z����U�"J)���BB("A�V�� ���B%�Rr)��co}�]���*[#D�Is�}�Oᖚ"�9�:�=�W����5	46ؙ�Kh��̕�AkM�X�� ��	l��������Y�h��aX��1lnӲ,	b	 � ��d"��ó�>�*�A��׶��M|h�-�#XXXdӄa��66S��g���-˄�d_o�sS��S�����js+�];a͢\"������G#YYY���k�p���	����p^*?�R�Q�?G�ˠ`sq���Ⰽ�p���m����vc6�8ib���Qaɯ,�%T���V���lk�y�d�=��r`w��|L�Hj��=8��5�,M�P���Xw���~I0yce`�8K	#<a� ��]�kF�������w�	^�~�Z�W�� �$�M1���@:���RFD[|��By �.�£��C2��`�-%SNT�֌F�/@[~��o��t#YYY� v�-	"�.5[ ��?B�F0i�Z/Qp�j����������_��VM�d��g����`��p�H׌�u$us���NQ� �ֵ���0~�D� ���64�~~�:��=�a��/a�����u~���baч���?�W����;3�6�	�������B� 0�ff1�8I��MlD&����HC��m&c��d&�����i�g�S�Ѧ����-�J+ԖB�3�'�ժ�_X��b��e�̇X n5���eM�A�g��V��������I~�p J,���:��qv�8#!��)�P�g(x�TcC?� 1�r#YYY����'9����F��x"8���Xt��PC�m���S?Qwm�Mٜ�6�뙖�D�#YYY�=���fņq�Q�EY���qPѴ��1��$��ŉ���Q	ҙ�(���^���4l%)��6�n�}����"-�7t�̓�F,�	#YYY�W�r�z�ss�:p�JaLv�6���@Dp�"��+����PXd��vXe��D�Q�c���n��@D=8QL̹���6�ަ��Ac�h{�q֙1�!���7o"���̏6�9�V�,�����SG<�9s�����]w�uc���ܼ�.���twW��-����G���X���ݠ��c%�^�16h;t�r&+ׇ��t��,�����,Q|�lp{Y�{���P��Q%�L�Vs��r� ��O��=�_n���E��x��CH&��w��c�^�����F:�~��Dc�c4H���H�J���Ë�$!\0e":����Ry�2�,��y#YYY��t�\w��G�6�l�/�Q[�,t��I�H(u�HG]=��N3ɾp#�|�c�f��(s����b�xR凁��\��ŉ�燙;�n���"��7��ZZ,�H�	��g�p_��o&�V.{�׮��#�6ᄞJ͕��^�2X��8�1��q�(K�(�9�v2@=�&	�?zQ���-<h@��X����`F�H���( X�9/��HYT����T�A#�9�壑��Xㇶ�(��	73N}��3tm0.o��he��U�zj.Z8�'"h����ӏ�ܳ��5��hF�i08����Rؼ�"�+f7�LdqC�p��4�C����#YYY��5<��$��t!e�S"����Cl���c��G��m>g-v{~<�r����C�8w�>.��5G�����hq�A�M�����܅���-ż�jQ��틇�Q�" ���+����M�]���2�N-�&b�1u���p�~��,h�Y��7�#XXX'�ܛ����C�]	��'4�Y������T�Y$���O?."�kM7ˌ�-��?,���4��莚Cc�f"[���'IO���m/�~=g ^�s�,�F��#YYY�Z7J����]�,�c��p1w|L�T�Ԑ����K݄fI~}�bG��\�A�uא�eG- �A���v�S�w� K����~�1���V��S���ʀ�Wh40F]�}��B�6��^���w�TG�-e�W�(:g��n��i�2��9�V����xh�!6���A�&�tt��b��(E�8[3J���'0G<'ml4pf78_1�v�hQ$I!=z�ˣ�v�&��|��x��ûh����G-FMdp�:F�z�;^� 6��Mf�ƶ��FItAL<GG��D7m�Q�P:ߏS�����g&�8;g�^T�s2_���ը��㹃�Fm�^�5q������Ǥ�7��H49��A˰�Bb�)�N#YYY�&���>����#QD���V�{�sh��INP|X`&����z������dFI�y�������֘�����cD��F���fdH��i�,m�-�	"R!�#4����5�]Z����"�ebw �H89�1}7KN�za��1��~�t�rY�оm�CӓIҒsI�PZLܘH��s���1�zf��j�6��7�ioUc?!��li�r	ytN@JP.k���5�k�sN2|��@.��Sa���|jd��X%NHt$0�3e���w��;~ߕ�^)Gf�$�e���E��y2w�����m+!|ӵ��4�4N4mGm5&Y~ɸq�;e�C�U��W��0g|EF����p,"@iZb��'��+(f*������\�뜵�p�������t�C���i�;�sd�a;%��1�]�Q�������#XXX w1�A���bN낳�;��C�$���P��},�(�b�����r���� ��5����Q,5�v	�.�`��P�B.��&��n�X�Iv��^��x٥�H#YYY�����?�dk��5�H�,�e������ߗYw~�1��4�]�k�6�#�{}�K\�3� ~��x��$}����/e�ʒ�X'�0��#�VĿVxu?��G��`0�ө `�3�db�$�'���� h��@0`��`�f9�:�"��eL4ᓔ@d�80V�p(�T5��f`;HPP�2R�2bI��ÿϣ�:�|p��#YYYB�.���.H/E���n4<�Y`��'��|��8������/b^zH.Ј�C�dn*6֒��݊��q�xY�~ZF}���*Ƹ���N�+x��G<&q�_(�����f��1lc�B�~�j����v��#YYYJV�¥n֛)��b`��X��W���I����5ā�D��N�'�!� ������dI���+z�à�9w�.'�Ɉ9X<�I]S��d�+�ɨ�Jw`8�bH����{�N>Rv��p�'/@{�9�S"�,�8q��oׄ��ql��0I$i�C3�	5������W�4�a`�l��U��1����l��Ҟ��]>�nb:�#YYYޫ�#YYY�!r��7�����!$!揞#YYYBRA�{0�Zc11@c#"���0���Hd��[N����d��&KKA�h1%ԏ�*��<!��_�I�>S�5z&I@S2%% �M=!p�" #XXXi(�Ի���\���3An��� ���(i�O].��qd#�נ�'`⠢"��*J����`T1�&���ّ�J;CK�Rp��J�y�~WO~����q�-�xH�Vڞ'����M�#��e2��:`�#5�M� ��r��0Ճ�{��ŬREةPJ8�i���3?��<A���lc�'��DG������@��sՁ�{pǦA������"���}4R927B����|���\�e��u���7�v6�m���F5IX��`_8bu�bn	ā%'s�GM��>�*�$����yX������:������v�	�2)��^LU�Z�(��S�|8�@cq�9:���������޳I�4��|FV>���|�}|�p��*4�h[��n�� 0CH'�O��NF�nq�C�t���v��Vg��<�h��7G�Ɉ&���!����f�Y���#���ݷ�}.�� :P�~%@ڼ~��e�A8�g������k�H0��y����cD�J[�y�:ރ����n��OHJ��L�~����wC�\�w[Ǯ��=/E�;J��.�v�����:>�w�����sA񂨤)� (��  %�I)%&$D;�#XXX�����b]�"0O z���;o�>��x����#2G�!YH`1IL�fbZ'�G�#YYY����ĢF� �#YYYa-UJ���.V��D�c��X̃ O�����(~�H���U��v��f�^l�A��s,nvX.\��#�/0uD9Q�3͑���a��A�b����s��=y�M*�q��� e���L��tM�ny�x#�mn�w�y��A��&#YYY�8�8k�bp�rD�&1>�ʂZN��PDd�T�I#XXX7�2�9�t�!���t4�:�qL�?����<�v�۬xB�]]#1���>�����7Zy�՜����;y�M�ǜ�	HX� ��AU��I��rחH��Tv�y��#YYYFf�'I�X偉DnF�ɝ��&�vZ���:�T`��h�k 2&$����l:O��j#�E��\��8�PvwU�Խݽؘ�^���0��ܟ{������:z3�;�"�8~_!�vE5�&|<AN�|{���ŎmeQ�a,@��g�W̭l��fN54�����1�����`��_&��ׅ��D	NG\lŉ��$e! Ha#n�Li�i%�)K�I���KK1�@E1)��^��<��������z�}���{y�@9Ǜ�&!�(�(k��^^1�s#XXXO��Y�Z�*Ħf.%�D�9��D$TmE��0F��^v�#�F�v���Xov���H��|JR�_g��A�������o�4�h��t�cJV�6a?x}�d�7�����1*~�)KP��pi�������p���y�<~���7��ǥ�'�,k���͐�ӱ�l��IuZٚ5��;��[A��Q"��ʈo h�T���<p�y?�ϖ���Ts�3� �ZP�8���A��0�v�v�H&��Lp#XXX�"݅D��1����M������`��<�:�.�=]�H1HGޟ����}���9�R�ӟt���1p�l<�,��<�����in�Y�|�N�9��<�[��ĨbT#"���#JZo�4�Ŝ�v�uam�On�1���B"A��QC0&d�S�Z3)*X$9��&/����G�����zB�J��U&��`���Y8Sr�_X�0�,���]���s�e)���[�q�8��,t����	P&�%�岦(]�L+�E'-N٩�@.��-h���Z�r6`ЗEYr�Ƿ#�|��L}MO���L�Lm��U�cϺ	�o{�	4�fA����¶d!�"d�1��m?��������#XXX1<1卲�(P�]��ͨ�4�4"'Q��ްc��'�|��!�ff���e���oF*˩Ѵmk���(�"*%���m$`cR��嬲A�ˎ�Æ�k!�p�BZ+jCr�Ɵ��0i���h��#YYY�1s,i��##XXXd��Kg���G}<H(�{#��#YYYm�h(´�Z��遉����rEi\��3i#YYY�ܒ7��H�p5�F������I�i�(~ntij������8�Y9D�N�@B�z�j��((�5��+2�$EN.ȅ#XXX���)��Q���#XXX�����j���v#Z6#XXX4����졲���%��b((!�����)m�z�ט0���F�4O7��s��s�W-$#XXX5�#XXX�D5��G=��1SMM	BP�R�&ה��y]�M��X_d���>�(]�ϖ4Q��!y�5�y����ok���y��r��=�f��۬fk�.P����ਹzn�u��{��j���Gu�����j�6#YYY�M��n��&4�̑��H:i%4��"u����)��M�((������Ł$�bM���h"0!y��=Z��g�c��d�&�h�<a��z#XXXp�݉;�x4}�(�b�Y�����S?AJF���N�ԍ�j9[��H�CAN�!\��1�u�k]#YYY&�~꟡�w��#XXXP�h#XXX��41*U,U�^���$�>yNC������S�H�I�E�!KHL`˨�0��H1I ���`���.�N�(��������i���Dxv�[��� �� 2S��#C0�ǌ����{'��Z�>i�A�cL���,T�E*��Pd��L�SJtp�3#XXX�b���_YJ��k�:���+(��ߜY5?��y�p��w����"�B�w��I;�zl�(�W����0�_g�q/xA�=�����\���DR;AI�0FaP	�C����JR���,$���,��*[͊Ôj1:G���C*ɢ�(��?<���1U�ӝv�Qb�"�Н}^�C�-���Fx�ǋ�ם�40�CLSm�b�����Ŋ6����u�9%�Wt���O~���?�����A�Z���>R {oǥ�!nr<�`��T����`��x9PF�xNC�_�G����y��:�;wwL<��r�mb�,�'�^�^�;	R(H�U�~xi�f>�1nC#XXX>�-?2����9"���F0b�2�F4d	�&����ɶ�B��~���:l�'�>yR9D6@����9��Xp�|�>g'��qv�����U�@n�:�E9Y�j}2#YYY��ay8P���%ԝ�i]6��#XXX.��8h9��x�C����j{��pE�'��)ND����M�#cx�I�|{G���uXܒF�#XXX�ʞ'F�5��j���(�C <6^Ώ��1��,o��և���b�Pà6#XXXe��� ����v����ڳ��5}=+�¶Y@�Z}�z%�:p��d<��#XXX��M��>��2��̢Y�א4V��d|��/i�B$��4�N�?gމ�(����u��U5M3�p��7с0`}��=�c���%d���)�22��&�h�h�Ȓ�d�ȈH� �L�%2Wh��$�RPd�FE�jҴj2�&���#}a�hShL���m��@���C���كF)�N��jJ"���*�#YYYD�a=Ƃ��b*)���"S#m#�&�	q:llj�"k,�t�b{o��Ȋ�A�:H�T��$H�������q�ej샬�I�'ƞ�6��C~�O^/�h6��N��#YYY��M�u��I�,Ca!hW%m��L��W����뇄���z~I!!lvL����c�|��Y k���q��G�^#YYY�|��C���F����ρ�0�ކ� ��;� �yx��ӷA>���)�	S����.E����:��:���=U�LjF{���Pa�2a�$���2I�1����m��\�kj�;{O#�U�O褴��y����\�1�Ji�#YYYu����g([�{���+���(1 ^sFSh��X���'��	��vA��:�#Xj�׬t�C&0��X���#XXX ���#'P�+|a6A2*H#XXX��������>]�u�Z�wA�$���I%Y;�A��5;���i�W=ag�>^�#XXX�*��F���q��gO���b|��S��#XXX3�0,�V���}J�Ӷ�RnO���5���y�8낣.BAA�؁�~kd	����A*#����a�h��9��]�E��:���A��LS<����Lr��8L��1�2�%m�q2���a�5�O��.�� Pi��)�]����� )2`\DBe�s&���14Z�#XXXQ�<E�(�a�8�D&�4���$̃�8�*�������OO.��G��0D���I#XXX�{&	o�@$4���p��^���P;,��9�2����s},����b�\�śg]�U��e)�]�ԉ�a�B�xꬊ�":�����/��O{0��a�ܽ��9LJ�qXb\�1�"�S8A|�x&Ȃ6��.p\�C�c���9=ډf�{�pl���R�ӟ�N1��uu���h�^O���<���.��l����y�����0����@�R@Dtn�Do���fj ((� Qk�����ARUv�NѰ�z�Z�G^��O�����{v^R\!&��U�b��t �!#YYY1�yf�U�&�� @�T'U��C2C��(z�ܾ�f�b8-^a��#YYY0chP0^C�#XXX`�ڱ�g���k��/�̾h��b��u�Q}���׷K��H�����{-#YYY������-E�3�^�4c��7�ֶ�ґ *;��Ϡ�=\�/��H��ߏ.CP��K?�4{��m�bB3�~�JJ; ϴr�7����5�qi�!])���F�Ϟ����Ö�cq�����7a�ݘ�u��q��劳2�0u*kWh�#M��A���j������>�����^$=>�6#YYY;�[� �Q�&��*JB�bQk��N��?-�4��"��&��0�{���}6�Z�ݑ�9��o�g,���j��L�{- jL�Aݬh#YYY{����>nȈ��ue��-U�����lC�¾r#XXX"B���A����w���!���^����e�N-f|��Φ14ogp��5���Ϯ���<TԩT�$�e�3(HP�a0�`�r��,%i���Tn8{p�L`.]An��#YYY�50aZ�1�A�	�j�.�(.Σ�"<�����̗R������y/J����mS����@��e*�nx:c$d`��#YYY����|\;���v�tE-w1�RI�̌Zʚ��&���ه=�v��tQ��u�K�W��R�|T�=/�����ċ ����øN?���Ԗ~su�,H�Gȕ���8���>aɑη����=;b�u�8y.t�Yۡ��E���D���x8�����B��1a�_���) �^/�qz鄠�!�78f����2{�`�)�l#N$��={��%���9�˪�<x�~�0ٺ�kF��-\�0�`i�����7&���RC� C���5 �	�7oR��#�VB-0T�#YYYҤP��U��;�%)ܙ��(��h�cC�2��w\d.L�q���2�=6A���7�,Y��Lׇ�����ǫli��>k�����y����TF�kV�3�+��5'c��t��`��3	95�)#�cB�i�NH&^�#XXX�s����A�#���u�_��)Ŋ��E[k{�=x��#YYY��Sl]2�D�\��}}�V,]�M�CA�����7*٦6�QR)�Ċ�'g�,pgB)�m��cC44@�e�œ������B� 4�1 a��>o��ў�G�6V�	7�����n3� l�s���3�ڜ'�����ܽ����,m�_���vk��+�9�U��#YYY�1��F�E#RO�BB3�Ys-�k�#XXX�ޙτÍqφ�}g�ȋ�U8[=����}#�p���&�VDpFΣ�m�[F&a��d�Q�͒&nn\��s����f�ص6i�Xi��:���'n��_�Hs~:7~ ��*'W��x��;��|%P�#XXXħl�ۻ�#XXX��I-�p	��pぇ��>�sڜ��{���_~7�|{��+ះ��(������2D�'>L���4���݌�>YS � J*�M�8E�Z;` ��G䓺D�B��i(~i�F�8�i�x6�@DzZ�Hj����#YYY����/�e�����U�cv[���JQ@"�� � �(�6Ƹ��uE�tlQ�!�I(1��q�9%dJU@|�H������oEq�GF�G���>��ǻ�5<�>�̲�1R��#XXXU�o��%{5�v˴� ��'����F�9�����`�,EI%P�������������33,N���A�~�f�&~w�Z�H�o7Ng�<$~ �93�c��x9��� ��T �����'i��	�L��N��=G,ӱ�;$C��v�F#YYYop�V�t'vw�#��?a�,��(་7ȃQ��݌c�&ǚ���%#XXXFk8MHPF{���?��G�����Q�E�m��I "S,fjięQ���I	n����}/��%:j���h�J ���̡)�N��s{� t���i��'+lR�0g��#�8����1Qr�8�H�xc�K~��8�|>[�̞���K[^(�m�%�M8^]�hvN$���?M�m|�z(���4�����9���#��!�Ŕ�8n ���~����HP�U9tdF���˫�z�Ϙ����Ld���<i���٣٦�c����)�%��)1(�ᗷ�~�Î���}���֤�cjjrN/�I�g4���c�A�"��%XkJ��)�?3@�.�~�o�xPZ3�'s�L00��G�pY��se���UiGm�N��c������Ou�;����+w[�Hd�������qؖ�a�J��LIf�qb�aE�����SWi������׋�����q�%0.�o��ճ.�;�O�%X�%=�F,Ď�4����6�>��TŅ>P<��\���f��9�����%��_�฾s�p\��5�B��������Β�/I�S��Y>�6v�d0"�cl���L����	���w����>@]_#YYY�N|�f��vPhm�c/��C,85�,�~4�b	9� ``�0y�̆cJ�k����`_eA�k4K �#CW�᳣EЈ�d��S璼E�v��X�(2�[m��t����u'��B�$:K(�����l[/���|�[bC��!h�	��O���X~�Q�?�$��ZW�z��rE8P���n�
#<==
