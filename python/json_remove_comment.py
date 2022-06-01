# -*- coding: utf-8 -*-
'''Python3 去掉json中带的注释
'''

import re
try:
    import commentjson
except Exception as e:
    print(e.args)
    print("commentjson not found. Please install it: pip install commentjson")


def parse_json_str(jsonStr: str):
    pos = 0
    bPos = 0
    flg = '/'
    isMathModel = False

    while (True):
        pos = jsonStr.find(flg, pos)
        if pos > -1:
            if isMathModel:
                jsonStr = jsonStr[:bPos - 1] + jsonStr[pos + len(flg):]
                pos = bPos
                isMathModel = False
                flg = '/'
                continue

            lineBeginPos = jsonStr.rfind('\n', 0, pos)
            lineStr = jsonStr[lineBeginPos:pos]
            num = len(re.findall('"', lineStr))

            if num % 2 == 0:
                if jsonStr[pos + 1] == '*':
                    flg = '*/'
                    isMathModel = True
                    bPos = pos
                    continue
                elif jsonStr[pos + 1] == "/":
                    lineEndpos = jsonStr.find('\n', pos)
                    jsonStr = jsonStr[:pos - 1] + jsonStr[lineEndpos - 1:]
                    continue

            pos = pos + 1
        else:
            break

    return jsonStr


if __name__ == "__main__":
    json_str = '''{// 中文
    //  test
{
  // comment11
  k11: "v11",
  k12: "v12",   // comment12
  //comment13
  k13: "v13",   //  comment13   

  /* comment21 */
  k21: "v21",
  k22: "v22",   /* comment22 */
  /*comment23*/     
  k23: "v23",   /*  comment23*/     

  /* line311
   * line312
   */
  k31: "v31",
  /** line321
   * line322
   */
  k32: "v32",
  /**
   * line331
   * line332
   */
  k33: "v33",
  ke:0
}
}
'''
    print(f"before json:\n{json_str}")
    result = parse_json_str(json_str)
    print(f"after:\n{result}")
    result = commentjson.loads(json_str)
    print(f"after2:\n{result}")
