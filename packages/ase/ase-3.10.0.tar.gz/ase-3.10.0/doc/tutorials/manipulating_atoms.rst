.. _atommanip:

Manipulating atoms
------------------
We will set up a one layer slab of Ni atoms with one Ag adatom.

Define the slab atoms:

>>> from ase import Atoms
>>> atoms = Atoms('Ni4', [(0, 0, 0),
...                       (0.45, 0, 0),
...                       (0, 0.5, 0),
...                       (0.5, 0.5, 0)])

Have a look at the individual atoms:

>>> atoms[0]
Atom('Ni', [0.0, 0.0, 0.0], atoms=..., index=0)
>>> atoms[1]
Atom('Ni', [0.45, 0.0, 0.0], atoms=..., index=1)
>>> atoms[2]
Atom('Ni', [0.0, 0.5, 0.0], atoms=..., index=2)
>>> atoms[3]
Atom('Ni', [0.5, 0.5, 0.0], atoms=..., index=3)

Let us assume we forgot how many atoms we set up:

>>> atoms[4]
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
IndexError: list index out of range

Wrong because we only have four atoms

>>> len(atoms)
4

Change the position of the 2nd atom in the list

>>> atoms[1].x = 0.5
>>> atoms.get_positions()
array([[ 0. ,  0. ,  0. ],
       [ 0.5,  0. ,  0. ],
       [ 0. ,  0.5,  0. ],
       [ 0.5,  0.5,  0. ]])

What is the unit cell so far?

>>> atoms.get_cell()
array([[ 1.,  0.,  0.],
       [ 0.,  1.,  0.],
       [ 0.,  0.,  1.]])

Now, setup a p(2x2) cell in a hexagonal surface.
Here, *a* is the fcc lattice constant, the cell is 10 layers high:

>>> from numpy import sqrt
>>> a = 3.55
>>> cell = [(2/sqrt(2.)*a, 0, 0),
...         (1/sqrt(2.)*a, sqrt(3./2.)*a, 0),
...         (0, 0, 10*sqrt(3.)/3.*a)]
>>> cell
[(5.0204581464244864, 0, 0),
(2.5102290732122432, 4.3478442934401409, 0),
(0, 0, 20.495934556231713)]
>>> atoms.set_cell(cell, scale_atoms=True)

The argument *scale_atoms=True* indicates that the atomic positions should be
scaled with the unit cell. The default is *scale_atoms=False* indicating that
the cartesian coordinates remain the same when the cell is changed.

>>> atoms.get_positions()
array([[ 0.        ,  0.        ,  0.        ],
       [ 2.51022907,  0.        ,  0.        ],
       [ 1.25511454,  2.17392215,  0.        ],
       [ 3.76534361,  2.17392215,  0.        ]])

Plot the whole system by bringing up the :mod:`ase.gui`:

>>> from ase.visualize import view
>>> view(atoms)

.. image:: a1.png
   :scale: 35

Within the viewer (called :mod:`ase-gui <ase.gui>`) it is possible to repeat
the unit cell in all three directions (using the :menuselection:`Repeat -->
View` window).

.. image:: a2.png
   :scale: 35

We now add an adatom.  Since the supercell is now declared as the unit
cell for our atoms we can either add the atom using its cartesian
coordinates in Angstrom or rescale the unit cell and use scaled
coordinates. We try the latter:

>>> from numpy import identity
>>> from ase import Atom
>>> xyzcell = identity(3) # The 3x3 unit matrix
>>> atoms.set_cell(xyzcell, scale_atoms=True)  # Set the unit cell and rescale
>>> atoms.append(Atom('Ni', (1/6., 1/6., .1)))
>>> atoms.set_cell(cell, scale_atoms=True)  # Set the unit cell and scale back

The structure now looks like this:

>>> view(atoms)

.. image:: a3.png
   :scale: 35

------------------
Interface building
------------------

Now try something else. We will make an interface with Ni(111) and water.
First we need a layer of water. One layer of water is constructed in this
script :download:`WL.py`, and saved in the file 'WL.traj'. Now run the WL.py
and then import the atoms object from the traj file using read.

>>> from ase.io import read
>>> W = read('WL.traj')

Lets take a look at the structure using view.

.. image:: WL.png
    :scale: 35

and let's look at the unit cell.

>>> cellW = W.get_cell()
>>> print(cellW)
array([[  8.490373   0.         0.      ]
       [  0.         4.901919   0.      ]
       [  0.         0.        26.93236 ]])

We will need at Ni(111) slab which matches the water as closely as possible.
A 2x4 orthogonal fcc111 supercell should be good enough.

>>> from ase.lattice.surface import fcc111
>>> slab = fcc111('Ni', size=[2, 4, 3], a=3.55, orthogonal=True)
>>> cell = slab.get_cell()

.. image:: Ni111slab2x2.png
    :scale: 35

>>> print(cell)
array([[ 5.02045815  0.          0.        ]
       [ 0.          8.69568859  0.        ]
       [ 0.          0.          6.14878037]]

Looking at the two unit cells, we can see that they match with around 2
percent difference, if we rotate one of the cells 90 degrees in the plane.
Lets rotate the cell

>>> W.set_cell([[cellW[1, 1], 0, 0],
...             [0, cellW[0, 0], 0],
...             cellW[2]],
...            scale_atoms=False)

.. image:: WL_rot_c.png
    :scale: 35

Let's also rotate the molecules:

>>> W.rotate('z', np.pi / 2, center=(0, 0, 0))

.. image:: WL_rot_a.png
    :scale: 35

Now we can wrap the atoms into the cell

>>> W.wrap()

.. image:: WL_wrap.png
    :scale: 35

The :meth:`~ase.atoms.Atoms.wrap` method only works if periodic boundary
conditions are enabled. We have a 2 percent lattice mismatch between Ni(111)
and the water, so we scale the water in the plane to match the cell of the
slab:

>>> cell1 = np.array([cell[0], cell[1], cellW[2]])
>>> W.set_cell(cell1, scale_atoms=True)
>>> p = slab.get_positions()
>>> W.center(vacuum=p[:, 2].max() + 1.5, axis=2)

Finally we use extend to copy the water onto the slab:

>>> interface = slab.copy()
>>> interface.extend(W)
>>> interface.center(vacuum=6, axis=2)

.. image:: interface-h2o-wrap.png
    :scale: 35

The positions of the water in the slab unitcell will be the same as they had
in their own unit cell.
