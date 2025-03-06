

**************
Proofs of seL4
**************

.. admonition:: Resources

    - `Introduction to the seL4 proofs <https://youtu.be/AdakDMYu4lM?si=vj6CegZksKi5OVAY>`_
    - `FAQ: What is formal verification? <https://youtu.be/AdakDMYu4lM?si=vj6CegZksKi5OVAY>`_
    - `FAQ:  The proof <https://sel4.systems/Info/FAQ/proof.html>`_
    - `Comprehensive formal verification of an OS microkernel <https://trustworthy.systems/publications/nictaabstracts/Klein_AEMSKH_14.abstract>`_


Interactive Proof Assistants
============================

Lean
----

- `Jeremy Avigad's lecture <https://sites.pitt.edu/~dgcole/HACPS/proofs/HACPS.lean>`_

Isabelle
--------

- `Introduction to seL4 proofs: Part 1 <https://sites.pitt.edu/~dgcole/HACPS/proofs/HACPS1.thy>`_
- `Introduction to seL4 proofs: Part 2 <https://sites.pitt.edu/~dgcole/HACPS/proofs/HACPS2.thy>`_
- `Introduction to seL4 proofs: Part 3 <https://sites.pitt.edu/~dgcole/HACPS/proofs/HACPS3.thy>`_

.. 
    - What are the proofs, and what do they mean?
    - Where do I look for them, and how do I read them?
    - How do they actually provide strong assurances?

    ------

    - What does refinement mean?
    - What are invariants?


    Introduction to Isabelle/HOL
    ============================

    `<https://isabelle.in.tum.de/>`_

    Introduction to Specification and Hoare Triples
    ===============================================

    Abstract Specification
    ======================

    Invariants
    ==========


.. at 4:44 in Introduction to the seL4 proofs:  Interactive Mode

..
    Define Hoare Triples
    --------------------

Look in ``lv4/proof/ROOT`` and you will wee a session that titled ``AInvs``.

You can ``Command-click`` on ``ArchDetSchedSchedule_AI`` to get the theory, ``ArchDetSchedSchedule_AI.thy``.  Or just go to ``l4v > proof > invariant-abstract > ARM > ArchDetSchedSchedule_AI.thy``.

.. code-block:: isabelle

    session AInvs in "invariant-abstract" = ASpec +
        directories
            "$L4V_ARCH"
        theories [condition = "SKIP_AINVS_PROOFS", quick_and_dirty, skip_proofs]
            "KernelInit_AI"
            "$L4V_ARCH/ArchDetSchedSchedule_AI"
        theories [condition = "AINVS_QUICK_AND_DIRTY", quick_and_dirty]
            "KernelInit_AI"
            "$L4V_ARCH/ArchDetSchedSchedule_AI"
        theories
            "KernelInit_AI"
            "$L4V_ARCH/ArchDetSchedSchedule_AI"

This loads all of the theories necessary to prove this theory.  You will see them on the right of the IDE.  It takes a long time for them to load and check them.  Go get a drink.

Building the Proofs
===================

.. code-block:: console

    $ L4V_ARCH=ARM make -C spec/ ASpec 
    $ L4V_ARCH=ARM make -C spec/ AInvs 

.. code-block:: console

    $ L4V_ARCH=ARM isabelle jedit -d . -R ASpec &
    $ L4V_ARCH=ARM isabelle jedit -d . -R AInvs &
    

- ``ASpec`` is in ``spec/ROOT``
- ``AInvs`` is in ``proof/ROOT``

Abstract Invariance
===================

The are found in the ``proof/invariant-abstract`` directory plus and additional directory for the architecture (e.g., ``ARM``).  The content is then in the top-level theory ``ArchDetSchedSchedule_AI.thy``.

Invariance due to kernel calls
------------------------------

.. code-block:: isabelle

    lemma akernel_invs:
        "⦃invs and (λs. e ≠ Interrupt ⟶ ct_running s)⦄
        (call_kernel e) :: (unit,unit) s_monad
        ⦃λrv. invs and (λs. ct_running s ∨ ct_idle s)⦄"

The pre-condition is that we are in a state where the invariant condition ``invs`` holds, and we there is not an interrupt ``e ≠ Interrupt``, thus the kernel is in a running state ``ct_running s``.

.. code-block:: isabelle

    P = invs and (λs. e ≠ Interrupt ⟶ ct_running s)

The post-condition is that there is a return value such that the invariant condition ``invs`` still holds, and the state is either ``ct_running s`` or ``ct_idle s``.

.. code-block:: isabelle

    Q = λrv. invs and (λs. ct_running s ∨ ct_idle s)

If it's running, it's in user mode.  If it's in idle mode, the only thing that wakes it from idle mode is an interrupt.

The command is a call to the kernel, transitioning from the pre- to the post-condition.

.. code-block:: isabelle

    c = call_kernel e

Invariance in the user space
----------------------------

We can also show that the user space preserves the invariants.

.. code-block:: isabelle

    lemma do_user_op_invs:
        "⦃invs and ct_running⦄
        do_user_op f tc
        ⦃λ_. invs and ct_running⦄"    

which shows that for the command ``do_user_op f tc`` we transition from a running state where the invariant holds to a running state where the invariant holds.

The state machine
=================

Open the ``ADT_AI`` theory. (Abstract Data Type - Abstract Iterpretation)

.. code-block:: isabelle

    definition
        ADT_A :: "user_transition ⇒ (('a::state_ext_sched state) global_state, 'a observable, unit) data_type"
    where
        "ADT_A uop ≡
        ⦇ Init = λs. Init_A, Fin = λ((tc,s),m,e). ((tc, abs_state s),m,e),
          Step = (λu. global_automaton check_active_irq_A (do_user_op_A uop) kernel_call_A) ⦈"

and 

.. code-block:: isabelle

    definition
        kernel_call_A
            :: "event ⇒ ((user_context × ('a::state_ext_sched state)) × mode × (user_context × 'a state)) set"
        where
        "kernel_call_A e ≡
            {(s, m, s'). s' ∈ fst (split (kernel_entry e) s) ∧
                         m = (if ct_running (snd s') then UserMode else IdleMode)}"

These show several things:

- User space ``do_user_op_A``
- Kernel space ``kernel_call_A``
- Interrupts ``check_active_irq_A``
- Idle mode ``IdleMode``

Beyond this, this state machine is too complicated to describe here.

The type of the specification (command)
=======================================

The command is ``(call_kernel e) :: (unit,unit) s_monad`` and if we click through the ``s_monad`` defined in ``spec > abstract > Exceptions_A.thy`` is a special type of ``nondet_monad``

.. code-block:: isabelle

    type_synonym ('a,'z) s_monad = "('z state, 'a) nondet_monad"

and ``lib > Monads > nondet > Nonet_Monad.thy``


.. code-block:: isabelle

    type_synonym ('s, 'a) nondet_monad = "'s \<Rightarrow> ('a \<times> 's) set \<times> bool"

It's a function type taking an input state ``'s`` and returning a tuple of return values ``('a \<times> 's)``.  It does more.  The state type ``'s`` is a parameter, which allows this to be used for different input types.  It returns a ``set`` of tuples, which allows the proof to include non-deterministic specifications.  Fianlly, it returns a boolean, which allows assertions in the specifications.

.. code-block:: isabelle

    definition valid ::
        "('s ⇒ bool) ⇒ ('s,'a) nondet_monad ⇒ ('a ⇒ 's ⇒ bool) ⇒ bool"
        ("⦃_⦄/ _ /⦃_⦄") where
        "⦃P⦄ f ⦃Q⦄ ≡ ∀s. P s ⟶ (∀(r,s') ∈ fst (f s). Q r s')"

The state
=========

``spec > abstract > Structures_A.thy``

.. code-block:: isabelle

    record 'a state = abstract_state + exst :: 'a

.. code-block:: isabelle

    record abstract_state =
        kheap              :: kheap
        cdt                :: cdt
        is_original_cap    :: "cslot_ptr ⇒ bool"
        cur_thread         :: obj_ref
        idle_thread        :: obj_ref
        machine_state      :: machine_state
        interrupt_irq_node :: "irq ⇒ obj_ref"
        interrupt_states   :: "irq ⇒ irq_state"
        arch_state         :: arch_state


Calling the kernel
==================

``spec > abstract > Syscall_A.thy``

.. code-block:: isabelle

    section ‹Kernel entry point›

    text ‹
        This function is the main kernel entry point. The main event loop of the
        kernel handles events, handles a potential preemption interrupt, schedules
        and switches back to the active thread.
    ›

    definition
        call_kernel :: "event ⇒ (unit,'z::state_ext_sched) s_monad" where
        "call_kernel ev ≡ do
            handle_event ev <handle>
                (λ_. without_preemption $ do
                    irq ← do_machine_op $ getActiveIRQ True;
                    when (irq ≠ None) $ handle_interrupt (the irq)
                od);
            schedule;
            activate_thread
        od"

The kernel receives an ``event`` called ``ev``, and it handles that event.  It then runs the scheduler to pick a thread.  Finally, it activates that thread.  The lamda function in the middle tells it what to do if there is an interrupt.

The invariant
=============

``proof > invariant-abstract > Invariants_AI.thy``

.. code-block:: isabelle

    definition
        invs :: "'z::state_ext state ⇒ bool" where
        "invs ≡ valid_state and cur_tcb"

where

.. code-block:: isabelle

    definition
        valid_state :: "'z::state_ext state ⇒ bool"
    where
        "valid_state ≡ valid_pspace
                  and valid_mdb
                  and valid_ioc
                  and valid_idle
                  and only_idle
                  and if_unsafe_then_cap
                  and valid_reply_caps
                  and valid_reply_masters
                  and valid_global_refs
                  and valid_arch_state
                  and valid_irq_node
                  and valid_irq_handlers
                  and valid_irq_states
                  and valid_machine_state
                  and valid_vspace_objs
                  and valid_arch_caps
                  and valid_global_objs
                  and valid_kernel_mappings
                  and equal_kernel_mappings
                  and valid_asid_map
                  and valid_global_vspace_mappings
                  and pspace_in_kernel_window
                  and cap_refs_in_kernel_window
                  and pspace_respects_device_region
                  and cap_refs_respects_device_region"


The current thread control block.

.. code-block:: isabelle

    definition
        "cur_tcb s ≡ tcb_at (cur_thread s) s"

Objects don't overlap
---------------------

.. code-block:: isabelle

    text "objects don't overlap"
    definition
        pspace_distinct :: "'z::state_ext state ⇒ bool"
    where
        "pspace_distinct ≡
        λs. ∀x y ko ko'. kheap s x = Some ko ∧ kheap s y = Some ko' ∧ x ≠ y ⟶
            {x .. x + (2 ^ obj_bits ko - 1)} ∩
            {y .. y + (2 ^ obj_bits ko' - 1)} = {}"


Zombie Cap
==========

