#! /usr/bin/python
# -*- coding: utf8 -*-
import base64
def decodeContent(content,filepath): #删除缩进(Tab)
    try:
        bytearray_str = base64.b64decode(content)
        binfile=open(filepath,"ab+")
        binfile.write(bytearray_str)
        binfile.close()
    except Exception as e:
        print(e)

    return


if __name__ == '__main__':
    b64content="CAABAAMAAADEQxoAewAAABoC/CciAzgOGgQVPnAgS2hDAFN0iQpuMFBoQwUMAxoE3wBuIFNoQwAMA1R0hwpyEDZqBAAKBG4gT2hDAAwDbhBbaAMADANxIH8jMgBTcokKU3SICjECAgQ9AiwAVHKHCnIQL2oCAAwCchBXagIADAFyEPRpAQAKAjkCHQAaAvwnIgM4DhoEpgpwIEtoQwBUdIcKchA2agQACgRuIE9oQwAMA24QW2gDAAwDcSB/IzIADgByEPVpAQAMAB8AtQ5Tc4kKchAragAADAIfAncAbiA9KScACwWcAgMFWnKJCnIQ9mkBAFNyiQpTdIgKMQICBDwCwP8oxA=="
    decodeContent(b64content,"checkSize.bin")