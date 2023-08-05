# ALS-WR : Alternating-Least-Squares with Weighted-λ-Regularization 

This is the code to perform ALS-WR as presented by [Zhou et al] 

The code is mainly inspired from [Mendeley Ltd]

-   *R* ∈ ℝ<sup>*n* × *p*</sup> = (*r*<sub>*i**j*</sub>) denote the sparse user-item matrix.
-   𝒟 is the set of available ratings.
-   Assume a low rank constraint *K* on the matrix : *R* = *U**V*<sup>*T*</sup>, *U*, *V* ∈ ℝ<sup>*n* × *K*</sup>, ℝ<sup>*p* × *K*</sup>
-   *U*<sub>*i*</sub> and *V*<sub>*j*</sub> denotes respectively the latent features of user *i* and item *j*.
-   *n*<sub>*u*<sub>*i*</sub></sub> is the number of ratings provided by user *i*.
-   *n*<sub>*v*<sub>*j*</sub></sub> is the number of ratings available for item *j*.
-   *J*<sub>*i*</sub> and *L*<sub>*j*</sub> is respectively the set of rated item by user *i* and available ratings for item *j*.

Objective function :
*f*(*U*, *V*)=∑<sub>*i*, *j* ∈ 𝒟</sub>(*r*<sub>*i**j*</sub> − *U*<sub>*i*</sub>*V*<sub>*j*</sub><sup>*T*</sup>)<sup>2</sup> + *λ*(∑<sub>*i*</sub>*n*<sub>*u*<sub>*i*</sub></sub>||*U*<sub>*i*</sub>||<sup>2</sup>+∑<sub>*i*</sub>*n*<sub>*v*<sub>*j*</sub></sub>||*V*<sub>*j*</sub>||<sup>2</sup>)

 **Algorithm**

-   Input : *R*, *K* (possibly an initialization of *U* or *V* with SVD)
-   Until convergence do
    -   For each user (in parallel if wanted)
        -   *U*<sub>*i*</sub> = (*V*<sub>*I*<sub>*i*</sub></sub>*V*<sub>*I*<sub>*i*</sub></sub> + *λ**I*<sub>*K*</sub>)<sup>−1</sup>*V*<sub>*I*<sub>*i*</sub></sub>*R*<sub>*i*, *I*<sub>*i*</sub></sub>
    -   For each item (in parallel if wanted)
        -   *V*<sub>*j*</sub> = (*U*<sub>*L*<sub>*j*</sub></sub>*U*<sub>*L*<sub>*j*</sub></sub> + *λ**I*<sub>*K*</sub>)<sup>−1</sup>*U*<sub>*L*<sub>*j*</sub></sub>*R*<sub>*L*<sub>*j*</sub>, *j*</sub>

  [Zhou et al]: http://www.grappa.univ-lille3.fr/~mary/cours/stats/centrale/reco/paper/MatrixFactorizationALS.pdf
  [Mendeley Ltd]: https://github.com/Mendeley/mrec/blob/master/mrec/mf/wrmf.py
