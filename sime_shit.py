import numpy as np

m_3 = np.array([[ 0, 0., 0],
                [1, 0, 0],
                [0, 0., 0],
                [0, 0, 1]])

m_4 = np.array([[0., 0, 0., 5],
                [0, 0, 0, 4],
                [0., 0, 0., 3],
                [0, 0, 0, 2]])

print(m_3.data)
m_3 += m_4[:3, 3]
print(m_3.data)
print(m_3)