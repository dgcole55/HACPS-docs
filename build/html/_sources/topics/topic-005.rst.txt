
**********************
Cyber-Physical Systems
**********************

.. Resources
.. *********

.. None yet.

What Are Cyber-Physical Systems?
================================

Cyber-physical systems (CPS) are integrations of computational and physical components designed to interact with and control the physical world. By using embedded software, sensors, actuators, and communication networks, these systems collect data from their environment, process it, and take real-time actions to achieve specific goals. Examples of CPS range from everyday applications like smart thermostats and autonomous vehicles to complex infrastructures such as power grids, medical devices, and industrial automation. By bridging the gap between digital computing and physical processes, CPS enable unprecedented levels of efficiency, automation, and functionality.

At their core, CPS operate through a tight integration of computation, communication, and control. Sensors embedded in the physical environment gather real-time data, which algorithms process to make decisions or trigger actions. Actuators then perform physical operations based on these decisions, creating a feedback loop for continuous adaptation and optimization. This integration enables CPS to handle tasks requiring precision, coordination, and responsiveness, such as stabilizing aircraft, managing robotic manufacturing systems, or monitoring patient vitals in healthcare. The adaptability of CPS makes them critical for developing intelligent and responsive systems across various industries.

The benefits of CPS are transformative, as they foster smarter and safer infrastructure, enhance industrial productivity, and contribute to sustainable development. CPS optimize energy use in smart grids, improve transportation safety with autonomous systems, and innovate in healthcare with personalized treatments and real-time patient monitoring. However, their complexity introduces challenges, such as ensuring dependability, addressing cybersecurity risks, and managing interdisciplinary integration. Fault detection, tolerance, and failure isolation are critical concerns in safety-critical applications, while ethical and regulatory considerations must be addressed. With robust design, testing, and security, CPS have the potential to profoundly impact society, improving quality of life and driving innovation in a wide range of fields.

Failures in Cyber-Physical Systems
==================================

Failures in cyber-physical systems (CPS) occur when the interplay between computational and physical components breaks down, leading to unintended or catastrophic consequences. These systems are designed to operate in complex and often safety-critical environments, making their reliability paramount. However, failures can stem from software bugs, hardware malfunctions, integration errors, or human factors. For example, a minor oversight in software coding or an unanticipated physical interaction can trigger a chain reaction of faults, as seen in incidents like the Therac-25 radiation overdoses and the Ariane 5 rocket explosion. Such failures reveal the high stakes of CPS design and underscore the importance of rigorous testing and fail-safe mechanisms.

One of the main challenges in CPS is ensuring that computational models accurately reflect the complexities of the physical world. Discrepancies between simulated conditions during development and real-world scenarios can lead to unexpected behavior. Additionally, CPS failures often have cascading effects, where a single fault propagates through interconnected components. The 2003 Northeast Blackout, for instance, began with a localized software failure in the power grid's monitoring system but escalated into a widespread power outage affecting millions. This interconnectedness makes detecting and mitigating vulnerabilities a critical aspect of CPS development.

The consequences of CPS failures can range from financial losses and environmental damage to injuries and loss of life, depending on the system's domain. High-profile incidents, such as the Boeing 737 MAX crashes or the Toyota unintended acceleration cases, have drawn attention to the risks of over-reliance on software without sufficient fail-safes or redundancy. These failures highlight the need for a multi-faceted approach to CPS reliability, including robust software verification, continuous system monitoring, and comprehensive safety protocols. As CPS become more pervasive in areas like healthcare, transportation, and energy, addressing these vulnerabilities is critical to ensuring their safe and effective operation.

.. topic:: An example of a CPS failure 

	The Therac-25, a radiation therapy machine developed in the 1980s, became a tragic example of how software errors in safety-critical systems can have devastating consequences. Designed to treat cancer patients with precisely controlled doses of radiation, the machine relied heavily on software to manage its operations. Between 1985 and 1987, at least six patients suffered severe radiation overdoses, some of which were fatal. The root causes of these incidents included a concurrency bug in the software, inadequate safety interlocks, and the reuse of legacy code from earlier models without proper adaptation. Overconfidence in the software's reliability and insufficient testing further exacerbated the risks, highlighting significant gaps in system design and validation.

	The failures of the Therac-25 had a profound impact on the fields of software engineering and system safety, serving as a cautionary tale for the design of cyber-physical systems. These incidents underscored the importance of rigorous testing under real-world conditions, implementing redundant hardware safeguards, and conducting formal verification of software logic. They also revealed the dangers of neglecting human factors and organizational accountability in safety-critical systems. As a result, the Therac-25 case became a cornerstone in engineering education, shaping modern practices for ensuring the reliability and safety of systems on which human lives depend.

.. table:: Examples of CPS failures

	==============================================  =============== 
	Event/Failure                                   Year          
	==============================================  =============== 
	The Therac-25 Incident                          1980's        
	Patriot Missile Failure                         1991          
	The Ariane 5 Explosion                          1996          
	Mars Climate Orbiter Loss                       1999          
	Northeast Blackout                              2003          
	Toyota Unintended Acceleration                  2009--2010 
	Stuxnet Malware Attack                          2010           
	Deepwater Horizon Blowout Preventer Failure     2010          
	Boeing 737 MAX Crashes                          2018          
	==============================================  =============== 

Other examples of CPS failures are given in the :ref:`catalog`


.. topic:: Lessons for Cyber-Physical Systems Design

	The CPS failures demonstrate that software errors, even seemingly trivial ones, can have catastrophic impacts in cyber-physical systems. These incidents have driven significant advancements in the fields of system safety and software engineering, emphasizing:

	* Formal Verification: Using mathematical models to ensure correctness in software logic.
	* Redundancy and Safeguards: Implementing fail-safe mechanisms to mitigate errors when they occur.
	* Comprehensive Testing: Stress-testing software under real-world conditions to uncover hidden flaws.
	* Domain-Specific Adaptation: Ensuring reused components are carefully evaluated and tailored for new systems.

	By learning from these past failures, engineers and developers continue to improve the design and reliability of the critical systems on which modern society depends.

High-assurance cyber-physical systems
=====================================

High-assurance in cyber-physical systems refers to the rigorous level of reliability, safety, and security required for systems that interact with the physical world, especially in scenarios where failures could result in catastrophic consequences. These systems integrate computational elements with physical processes, such as autonomous vehicles, medical devices, and industrial control systems. Achieving high-assurance means guaranteeing that the system behaves as intended under all conditions, including extreme or unexpected scenarios, through meticulous design, testing, and validation. The goal is to minimize risks, ensure fault tolerance, and provide confidence in the system's dependability and safety.

A high-assurance approach involves the use of formal verification techniques, where mathematical models are employed to prove the correctness of software and hardware. This ensures that the system logic is free of critical errors and adheres strictly to its specifications. Additionally, high-assurance systems undergo comprehensive testing that includes stress-testing, edge-case analysis, and real-world scenario simulation. Redundancy and fail-safe mechanisms are also fundamental, providing backup solutions to maintain functionality and mitigate risks in the event of partial failures. High-assurance systems often operate in regulated environments, requiring compliance with strict standards and certifications that dictate design, implementation, and maintenance practices.

The importance of high-assurance in cyber-physical systems cannot be overstated, as these systems frequently play a direct role in protecting human lives, critical infrastructure, and environmental safety. A single flaw in a high-assurance system, such as an autonomous vehicle's control software or a medical device like the Therac-25, can lead to disastrous outcomes. Therefore, ensuring high-assurance involves not only technical robustness but also cross-disciplinary coordination among engineers, designers, and safety experts. By prioritizing high-assurance principles, developers can build systems that inspire trust and reliability, even in the most demanding and unpredictable environments.

.. topic::  Attributes of High-Assurance Systems

	1.	Safety: Operates without causing harm to people or the environment.
	2.	Security: Protects against unauthorized access and disruptions.
	3.	Reliability: Performs as intended under all conditions.
	4.	Robustness: Handles unexpected inputs and stress conditions gracefully.
	5.	Fail-Safe Design: Defaults to a safe state during critical errors.
	6.	Real-Time Responsiveness: Meets strict timing requirements in real-world scenarios.
	7.	Fault Tolerance: Maintains functionality despite failures through redundancy.
	8.	Formal Verification: Uses mathematical proofs to ensure correctness.
	9.	Comprehensive Testing: Covers edge cases, stress scenarios, and real-world conditions.
	10.	Standards Compliance: Adheres to strict safety and quality certifications.

.. topic:: Procedure for Ensuring High-Assurance Systems

	1.	Define Requirements and Constraints:

		* Clearly document functional, safety, and security requirements.
		* Specify performance, real-time, and environmental constraints.
		* Identify critical failure modes and unacceptable risks.

	2.	Risk Analysis and Hazard Assessment:

		* Conduct a thorough risk assessment using methods like FMEA (Failure Modes and Effects Analysis), HAZOP (Hazard and Operability Study), or STPA (System-Theoretic Process Analysis).
		* Prioritize mitigating high-risk scenarios and failure points.

	3.	Formal Design and Architecture:

		* Use modular, layered, and fault-tolerant design principles.
		* Incorporate redundancy and fail-safe mechanisms at critical points.
		* Develop system models for formal verification and simulation.

	4.	Formal Verification:

		* Use mathematical methods to verify the correctness of system logic.
		* Validate compliance with requirements for both hardware and software components.

	5.	Comprehensive Testing:

		* Conduct unit testing, integration testing, and system-level testing.
		* Include stress tests, edge-case testing, and real-world scenario simulations.
		* Use automated testing tools for consistency and repeatability.

	6.	Implement Standards and Best Practices:

		* Follow industry-specific standards (e.g., DO-178C for avionics, IEC 61508 for industrial safety).
		* Ensure compliance with safety and security certifications.

	7.	Cross-Disciplinary Collaboration:

		* Involve experts from relevant fields (e.g., hardware, software, and human factors).
		* Ensure seamless integration and validation across all components.

	8.	Documentation and Traceability:

		* Maintain detailed records of design, testing, and validation processes.
		* Ensure traceability of requirements, changes, and testing results.

	9.	Continuous Monitoring and Feedback:

		* Implement real-time monitoring and logging mechanisms in the system.
		* Regularly review system performance and update as necessary.

	10.	Lifecycle Assurance:

		* Reassess the system after updates, modifications, or environmental changes.
		* Decommission systems safely at the end of their operational life.

