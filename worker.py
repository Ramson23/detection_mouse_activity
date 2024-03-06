import sys
from threading import Thread

import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from joblib import load

from utils.recorder import *
from utils.extractor import *

import logging
import io

logging.basicConfig(filename='qw.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('urbanGUI')

curr_condition = int(sys.argv[1])
start_flag = True
try:
    model = xgb.XGBClassifier()
    model.load_model('./models/xgb_model.json')
    scaler = load('./models/std_scaler.bin')
except Exception as err:
    logger.info(err)


def wait_input():
    global curr_condition, start_flag
    while start_flag:
        try:
            out = sys.stdin.buffer.read(4).decode('utf-8')
            logger.info(f'out: {out}')
            if out.startswith('con'):
                curr_condition = int(out[3])
            elif out.startswith('stop'):
                start_flag = False
        except Exception as er:
            logger.info(er)


if __name__ == '__main__':

    logger.info('start')

    rec = Recorder(*map(int, sys.argv[1:]))
    rec.start()

    logger.info('start Procc')

    t = Thread(target=wait_input)
    t.start()

    logger.info('start Thread')

    while start_flag:
        try:
            logger.info('start ждем')
            frag = rec.q_data.get()

            logger.info(f'con in proc: {curr_condition}')

            rec.q_changes.put([True, curr_condition])

            raw_data = rec.convert_to_df(frag)

            exc = Extractor(raw_data)
            exc.separate_activity_segment()
            features = exc.extract()

            sys.stdout.write(f'0')
        except Exception as err:
            logger.info(err)

        # try:
        #     features['section_rel'] = features['section_count_after'] / features['section_count_before']
        #     features = features.drop(['condition'], axis=1)
        #     scaled_data = scaler.transform(features.values)
        #     scale_feature = pd.DataFrame(scaled_data, index=features.index, columns=features.columns)
        #     logger.info(model)
        #     pred = model.predict(scale_feature)
        # except Exception as err:
        #     logger.info(f'model: {err}')
        #
        # logger.info(f'pred: {pred}')
        #
        # logger.info('start пишем')
        # sys.stdout.write(f'{1 if sum(pred)/len(pred) > 0.5 else 0}')
        # logger.info('start написали')

    rec.q_changes.put([False, curr_condition])
    rec.join()
    t.join()
