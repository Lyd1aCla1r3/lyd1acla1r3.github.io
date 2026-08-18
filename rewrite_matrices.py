import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/positional-encoding/chapter_05.md', 'r') as f:
    text = f.read()

# Replace q0
q0_old = r"""### Position $t = 0$ (`The`): $\mathbf{q}_0 = \begin{bmatrix} -0.08 & -0.13 & 0.21 \end{bmatrix}^\top$

$R_0$ is the identity matrix, so the query vector passes through unchanged:

$$
\mathbf{q}'_0 = R_0 \, \mathbf{q}_0 = \mathbf{q}_0 = \begin{bmatrix} -0.0800 \\ -0.1300 \\ 0.2100 \end{bmatrix}
$$"""
q0_new = r"""### Position $t = 0$ (`The`): $\mathbf{q}_0 = \begin{bmatrix} -0.08 & -0.13 & \phantom{-}0.21 \end{bmatrix}^\top$

$R_0$ is the identity matrix, so the query vector passes through unchanged:

$$
\mathbf{q}'_0 = R_0 \, \mathbf{q}_0 = \begin{bmatrix} \phantom{-}1.0000 & \phantom{-}0.0000 & 0 \\ \phantom{-}0.0000 & \phantom{-}1.0000 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} -0.08 \\ -0.13 \\ \phantom{-}0.21 \end{bmatrix} = \begin{bmatrix} \mathbf{-0.0800} \\ \mathbf{-0.1300} \\ \phantom{-}\mathbf{0.2100} \end{bmatrix}
$$"""
text = text.replace(q0_old, q0_new)

# Replace q1
q1_old = r"""### Position $t = 1$ (`quick`): $\mathbf{q}_1 = \begin{bmatrix} 0.35 & -0.17 & -0.27 \end{bmatrix}^\top$

The full matrix-vector multiplication, component by component:

$$
q'_1[0] = \cos(1) \cdot q_1[0] - \sin(1) \cdot q_1[1] = (0.5403)(0.35) - (0.8415)(-0.17)
$$

$$
= 0.1891 + 0.1431 = \mathbf{0.3322}
$$

$$
q'_1[1] = \sin(1) \cdot q_1[0] + \cos(1) \cdot q_1[1] = (0.8415)(0.35) + (0.5403)(-0.17)
$$

$$
= 0.2945 - 0.0919 = \mathbf{0.2027}
$$

$$
q'_1[2] = q_1[2] = -0.2700 \qquad \text{(identity, unpaired dimension)}
$$

$$
\mathbf{q}'_1 = \begin{bmatrix} 0.3322 \\ 0.2027 \\ -0.2700 \end{bmatrix}
$$"""
q1_new = r"""### Position $t = 1$ (`quick`): $\mathbf{q}_1 = \begin{bmatrix} \phantom{-}0.35 & -0.17 & -0.27 \end{bmatrix}^\top$

$$
\mathbf{q}'_1 = R_1 \, \mathbf{q}_1 = \begin{bmatrix} \phantom{-}0.5403 & -0.8415 & 0 \\ \phantom{-}0.8415 & \phantom{-}0.5403 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} \phantom{-}0.35 \\ -0.17 \\ -0.27 \end{bmatrix} = \begin{bmatrix} \phantom{-}\mathbf{0.3322} \\ \phantom{-}\mathbf{0.2027} \\ \mathbf{-0.2700} \end{bmatrix}
$$"""
text = text.replace(q1_old, q1_new)


# Replace q2
q2_old = r"""### Position $t = 2$ (`brown`): $\mathbf{q}_2 = \begin{bmatrix} -0.09 & 0.47 & -0.07 \end{bmatrix}^\top$

$$
q'_2[0] = (-0.4161)(-0.09) - (0.9093)(0.47) = \mathbf{-0.3899}
$$

$$
q'_2[1] = (0.9093)(-0.09) + (-0.4161)(0.47) = \mathbf{-0.2774}
$$

$$
q'_2[2] = -0.0700
$$

$$
\mathbf{q}'_2 = \begin{bmatrix} -0.3899 \\ -0.2774 \\ -0.0700 \end{bmatrix}
$$"""
q2_new = r"""### Position $t = 2$ (`brown`): $\mathbf{q}_2 = \begin{bmatrix} -0.09 & \phantom{-}0.47 & -0.07 \end{bmatrix}^\top$

$$
\mathbf{q}'_2 = R_2 \, \mathbf{q}_2 = \begin{bmatrix} -0.4161 & -0.9093 & 0 \\ \phantom{-}0.9093 & -0.4161 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} -0.09 \\ \phantom{-}0.47 \\ -0.07 \end{bmatrix} = \begin{bmatrix} \mathbf{-0.3899} \\ \mathbf{-0.2774} \\ \mathbf{-0.0700} \end{bmatrix}
$$"""
text = text.replace(q2_old, q2_new)


# Replace q3
q3_old = r"""### Position $t = 3$ (`fox`): $\mathbf{q}_3 = \begin{bmatrix} -0.01 & -0.08 & 0.15 \end{bmatrix}^\top$

$$
q'_3[0] = (-0.9900)(-0.01) - (0.1411)(-0.08) = \mathbf{0.0212}
$$

$$
q'_3[1] = (0.1411)(-0.01) + (-0.9900)(-0.08) = \mathbf{0.0778}
$$

$$
q'_3[2] = 0.1500
$$

$$
\mathbf{q}'_3 = \begin{bmatrix} 0.0212 \\ 0.0778 \\ 0.1500 \end{bmatrix}
$$"""
q3_new = r"""### Position $t = 3$ (`fox`): $\mathbf{q}_3 = \begin{bmatrix} -0.01 & -0.08 & \phantom{-}0.15 \end{bmatrix}^\top$

$$
\mathbf{q}'_3 = R_3 \, \mathbf{q}_3 = \begin{bmatrix} -0.9900 & -0.1411 & 0 \\ \phantom{-}0.1411 & -0.9900 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} -0.01 \\ -0.08 \\ \phantom{-}0.15 \end{bmatrix} = \begin{bmatrix} \phantom{-}\mathbf{0.0212} \\ \phantom{-}\mathbf{0.0778} \\ \phantom{-}\mathbf{0.1500} \end{bmatrix}
$$"""
text = text.replace(q3_old, q3_new)

# Keys
k0_old = r"""### Position $t = 0$ (`The`): $\mathbf{k}_0 = \begin{bmatrix} -0.15 & 0.10 & -0.04 \end{bmatrix}^\top$

$$
\mathbf{k}'_0 = R_0 \, \mathbf{k}_0 = \mathbf{k}_0 = \begin{bmatrix} -0.1500 \\ 0.1000 \\ -0.0400 \end{bmatrix}
$$"""
k0_new = r"""### Position $t = 0$ (`The`): $\mathbf{k}_0 = \begin{bmatrix} -0.15 & \phantom{-}0.10 & -0.04 \end{bmatrix}^\top$

$$
\mathbf{k}'_0 = R_0 \, \mathbf{k}_0 = \begin{bmatrix} \phantom{-}1.0000 & \phantom{-}0.0000 & 0 \\ \phantom{-}0.0000 & \phantom{-}1.0000 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} -0.15 \\ \phantom{-}0.10 \\ -0.04 \end{bmatrix} = \begin{bmatrix} \mathbf{-0.1500} \\ \phantom{-}\mathbf{0.1000} \\ \mathbf{-0.0400} \end{bmatrix}
$$"""
text = text.replace(k0_old, k0_new)


k1_old = r"""### Position $t = 1$ (`quick`): $\mathbf{k}_1 = \begin{bmatrix} 0.24 & 0.11 & -0.32 \end{bmatrix}^\top$

$$
k'_1[0] = (0.5403)(0.24) - (0.8415)(0.11) = \mathbf{0.0371}
$$

$$
k'_1[1] = (0.8415)(0.24) + (0.5403)(0.11) = \mathbf{0.2614}
$$

$$
k'_1[2] = -0.3200
$$

$$
\mathbf{k}'_1 = \begin{bmatrix} 0.0371 \\ 0.2614 \\ -0.3200 \end{bmatrix}
$$"""
k1_new = r"""### Position $t = 1$ (`quick`): $\mathbf{k}_1 = \begin{bmatrix} \phantom{-}0.24 & \phantom{-}0.11 & -0.32 \end{bmatrix}^\top$

$$
\mathbf{k}'_1 = R_1 \, \mathbf{k}_1 = \begin{bmatrix} \phantom{-}0.5403 & -0.8415 & 0 \\ \phantom{-}0.8415 & \phantom{-}0.5403 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} \phantom{-}0.24 \\ \phantom{-}0.11 \\ -0.32 \end{bmatrix} = \begin{bmatrix} \phantom{-}\mathbf{0.0371} \\ \phantom{-}\mathbf{0.2614} \\ \mathbf{-0.3200} \end{bmatrix}
$$"""
text = text.replace(k1_old, k1_new)


k2_old = r"""### Position $t = 2$ (`brown`): $\mathbf{k}_2 = \begin{bmatrix} 0.16 & -0.17 & 0.36 \end{bmatrix}^\top$

$$
k'_2[0] = (-0.4161)(0.16) - (0.9093)(-0.17) = \mathbf{0.0880}
$$

$$
k'_2[1] = (0.9093)(0.16) + (-0.4161)(-0.17) = \mathbf{0.2162}
$$

$$
k'_2[2] = 0.3600
$$

$$
\mathbf{k}'_2 = \begin{bmatrix} 0.0880 \\ 0.2162 \\ 0.3600 \end{bmatrix}
$$"""
k2_new = r"""### Position $t = 2$ (`brown`): $\mathbf{k}_2 = \begin{bmatrix} \phantom{-}0.16 & -0.17 & \phantom{-}0.36 \end{bmatrix}^\top$

$$
\mathbf{k}'_2 = R_2 \, \mathbf{k}_2 = \begin{bmatrix} -0.4161 & -0.9093 & 0 \\ \phantom{-}0.9093 & -0.4161 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} \phantom{-}0.16 \\ -0.17 \\ \phantom{-}0.36 \end{bmatrix} = \begin{bmatrix} \phantom{-}\mathbf{0.0880} \\ \phantom{-}\mathbf{0.2162} \\ \phantom{-}\mathbf{0.3600} \end{bmatrix}
$$"""
text = text.replace(k2_old, k2_new)


k3_old = r"""### Position $t = 3$ (`fox`): $\mathbf{k}_3 = \begin{bmatrix} -0.06 & 0.11 & -0.05 \end{bmatrix}^\top$

$$
k'_3[0] = (-0.9900)(-0.06) - (0.1411)(0.11) = \mathbf{0.0439}
$$

$$
k'_3[1] = (0.1411)(-0.06) + (-0.9900)(0.11) = \mathbf{-0.1174}
$$

$$
k'_3[2] = -0.0500
$$

$$
\mathbf{k}'_3 = \begin{bmatrix} 0.0439 \\ -0.1174 \\ -0.0500 \end{bmatrix}
$$"""
k3_new = r"""### Position $t = 3$ (`fox`): $\mathbf{k}_3 = \begin{bmatrix} -0.06 & \phantom{-}0.11 & -0.05 \end{bmatrix}^\top$

$$
\mathbf{k}'_3 = R_3 \, \mathbf{k}_3 = \begin{bmatrix} -0.9900 & -0.1411 & 0 \\ \phantom{-}0.1411 & -0.9900 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} -0.06 \\ \phantom{-}0.11 \\ -0.05 \end{bmatrix} = \begin{bmatrix} \phantom{-}\mathbf{0.0439} \\ \mathbf{-0.1174} \\ \mathbf{-0.0500} \end{bmatrix}
$$"""
text = text.replace(k3_old, k3_new)

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/positional-encoding/chapter_05.md', 'w') as f:
    f.write(text)

print("Replaced all sections successfully.")
