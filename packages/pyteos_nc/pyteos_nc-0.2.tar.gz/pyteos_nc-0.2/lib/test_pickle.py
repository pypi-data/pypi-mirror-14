import pickle
from create_gridded_data import A_h_fixed_rh_wmo


file_id=open('test.pkl','w')
pickle.dump(A_h_fixed_rh_wmo,file_id)
file_id.close
