


*********************************************
HACMS:  High-Assurance Cyber Military Systems
*********************************************

It focused on creating robust systems for critical applications, such as drones and helicopters, by designing security into the software from the ground up and isolating vulnerabilities through advanced architectures like the seL4 microkernel. Independent penetration testing validated that HACMS systems were resilient to attacks, demonstrating the potential for formal methods to revolutionize cybersecurity in both military and civilian domains.

The High-Assurance Cyber Military Systems (HACMS) program by DARPA aimed to develop secure, high-assurance software systems resistant to cyber-attacks using formal methods, which mathematically verify software correctness.  It was driven by the need to address growing cybersecurity vulnerabilities in modern, connected systems, such as drones, helicopters, and automobiles. Its primary goal was to create software systems that are inherently secure and resilient against sophisticated cyber-attacks, focusing on eliminating exploitable bugs through the use of formal methods—mathematical techniques that ensure software correctness and safety. The HACMS program sought to build trustworthy systems capable of resisting remote hacking attempts, thereby protecting against threats to safety and security. The program aimed to establish a foundation for developing high-assurance software that could benefit both military and civilian applications, transforming how critical systems are secured.

The HACMS program employed a robust methodology centered on **formal methods**, which use mathematical proofs to rigorously verify software correctness and eliminate exploitable vulnerabilities such as memory safety errors and unauthorized access. This approach ensured the software was free of common flaws that attackers exploit, enhancing its security and reliability. Instead of retrofitting security into existing systems, HACMS focused on incremental development, designing secure software from the ground up to achieve high assurance. To validate its techniques, the program used experimental platforms, including open-source quadcopters like the SMACCMCopter and Boeing's Unmanned Little Bird (ULB) helicopter, as testbeds. These platforms allowed researchers to demonstrate the practical application of formal methods in creating secure and functional systems, showcasing their potential to transform critical software development.

The HACMS program progressed through three key phases, each building on the previous achievements to enhance security and functionality. In **Phase 1**, researchers refactored the quadcopter's software using memory-safe programming languages and verified operating systems, creating the high-assurance SMACCMCopter. Rigorous penetration testing by an independent “Red Team” revealed no vulnerabilities, validating the effectiveness of the formal methods. **Phase 2** advanced the architecture by introducing a multi-processor setup and isolating unverified components within secure partitions managed by the formally verified seL4 microkernel. Despite granting the Red Team root access to less secure partitions, the system maintained its integrity, preventing any compromise. In **Phase 3**, the program further improved features such as geofencing to constrain system behavior and extended the HACMS methodology to other systems, including military ground robots and networked weapon systems, demonstrating the broad applicability of the approach across various critical domains.

The HACMS program underwent extensive security validation through rigorous penetration tests conducted by independent “Red Teams,” which attempted to exploit vulnerabilities in the systems. These tests consistently demonstrated that HACMS-built systems were highly resistant to cyber-attacks, maintaining their integrity even under extreme scenarios. This robust security performance highlighted the effectiveness of the program's use of formal methods and its secure-by-design approach to software development.

The HACMS program demonstrated the feasibility of using formal methods to design highly secure and functional systems, proving that mathematically verified software can effectively resist sophisticated cyber-attacks. Its success provided a clear pathway for retrofitting existing systems with advanced security measures, enabling the enhancement of cybersecurity in legacy systems without compromising performance. Beyond its military applications, the program highlighted the potential for extending formal methods to critical civilian domains, such as medical devices, industrial control systems, and public infrastructure. By showcasing how rigorous software verification can address modern cybersecurity challenges, HACMS paved the way for safer and more reliable technology in both military and civilian contexts.

Background and Motivation
=========================

The interconnected nature of modern systems, even those designed to be isolated, has significantly increased their vulnerability to cyber-attacks. This issue extends beyond traditional computers to encompass the Internet of Things (IoT), including critical systems like industrial SCADA systems, medical devices, and vehicles. High-profile examples, such as the hacking of insulin pumps and automobiles, illustrate the risks posed by this connectivity. In particular, automobiles, now essentially computers on wheels with dozens of embedded control units (ECUs), have proven vulnerable to attacks through various points like the on-board diagnostics (ODB-II) port, Bluetooth, telematics units, and even entertainment systems. Such vulnerabilities have enabled attackers to remotely control critical functions, as seen in demonstrations by researchers who took over braking and acceleration in vehicles, highlighting the urgent need for improved security in interconnected systems.

Modern vehicles rely on software for essential functionalities such as anti-lock braking, cruise control, and remote access features, making them susceptible to exploitation. Research has revealed how attackers can manipulate vehicle systems remotely by exploiting flaws in CAN bus networks and other interfaces. For instance, hackers demonstrated the ability to reflash software in ECUs by accessing the ODB-II port or using telematics units to bypass authentication protocols. These vulnerabilities are not unique to specific vehicle models but are indicative of systemic security weaknesses across the automotive industry. A notable example is the 2015 remote hacking of a Jeep Cherokee, [#]_ which led to a recall of 1.4 million vehicles, emphasizing the critical need for stronger safeguards in automotive cybersecurity.

.. [#] Unknown

The pervasive threat of cybersecurity vulnerabilities stems from the inherent complexity, flexibility, and connectivity of modern computer systems. Effective security requires addressing issues across multiple levels, including software architecture, implementation, user behavior, and physical security. A significant portion of cyber risks arises from implementation errors, which can be exploited to execute arbitrary code or steal sensitive data. High-profile vulnerabilities like the Heartbleed bug in OpenSSL and buffer overflow flaws in widely used libraries demonstrate the scale of the problem. The emergence of black-market “Exploit Kits” further exacerbates these threats by enabling less-skilled attackers to leverage known vulnerabilities. These challenges highlight the importance of rigorous software development practices and proactive measures to address cybersecurity risks.

Formal Methods
==============

Formal methods, long heralded for their promise to create software without exploitable bugs, have become more feasible due to technological advancements. The exponential growth in computing power, driven by Moore's Law, has provided larger memories and faster processors, enabling the intensive computations required by formal verification. Moreover, advancements in automation, particularly in Boolean satisfiability (SAT) solvers, have significantly improved the ability to automatically prove software properties. Over a decade, SAT solvers have demonstrated a two-orders-of-magnitude improvement in solving complex problems, laying the groundwork for even more sophisticated tools like Satisfiability Modulo Theories (SMT) solvers and tactic libraries that enhance automation in theorem proving.

The infrastructure supporting formal methods has grown richer, making them more accessible and practical for broader use. Previously, researchers had to create their own tools, limiting the scope and reliability of formal verification. Now, a wide range of robust, well-documented tools such as Coq, ACL2, Z3, and TLA+ are publicly available, enabling developers beyond the academic community to employ formal methods effectively. These tools allow for comprehensive verification of software properties and have become vital in tackling the increasing complexity of critical systems.

The rising complexity of critical systems underscores the necessity of advanced tools like formal methods. Developers at organizations like Amazon Web Services have adopted model-checking techniques to address the limitations of traditional testing, particularly for identifying rare but impactful design errors in large-scale systems. Formal methods excel at uncovering subtle issues in corner cases that human intuition or conventional testing might overlook. This growing reliance on formal methods reflects their potential to ensure higher reliability and security in increasingly complex and interconnected systems.

Formal methods are rigorous mathematical techniques used in software and system development to specify, design, and verify computer systems. These methods can be applied to both software and hardware, either directly on the implementation code or on higher-level models. The key strength of formal methods lies in their ability to produce machine-checkable proofs, ensuring a high degree of confidence in the correctness of a system. However, the effectiveness of these methods depends on the accuracy and completeness of the models used, as any incorrect assumptions may limit the validity of the guarantees. Despite their robust capabilities, formal methods are not universally applicable and require careful consideration of their scope and limitations.

The spectrum of formal methods includes tools and techniques such as type systems, model checkers, sound static analyzers, verified runtime monitoring, automatic theorem provers, and interactive proof assistants. These tools vary in the level of effort required and the strength of guarantees they provide. For instance, type systems, which are highly scalable and widely used in programming languages like C and Java, offer basic guarantees such as type safety. On the other hand, interactive proof assistants like Coq and Isabelle provide strong guarantees, such as full functional correctness, but are labor-intensive and require significant expertise. This range allows developers to choose methods that balance the trade-offs between scalability, effort, and the desired level of assurance.

Certain software components are particularly worth verifying due to their critical role in system reliability and security, such as microkernels, hypervisors, and compilers. Examples include the seL4 microkernel and the CompCert verifying C compiler, both of which were instrumental in the HACMS program. The seL4 microkernel, verified using the Isabelle/HOL proof assistant, offers strong guarantees of functional correctness and security properties like authority confinement and non-interference. Similarly, CompCert, implemented and verified in the Coq proof assistant, ensures the correctness of C code compilation with performance comparable to traditional compilers. These artifacts demonstrate the feasibility and impact of applying formal methods to high-assurance software, providing a foundation for trusted systems in critical domains like aviation and military applications.

Implementation and Results
==========================

The High-Assurance Cyber Military Systems (HACMS) program implemented a structured, phased approach to achieve its goal of developing secure and robust software systems. The program started with commercially available platforms, such as an open-source quadcopter (SMACCMCopter) and Boeing's Unmanned Little Bird (ULB) helicopter. Researchers used formal methods to refactor and verify components incrementally. For the SMACCMCopter, they replaced legacy software with high-assurance code, incorporating memory-safe programming languages and verified real-time operating systems like FreeRTOS and eChronos. The use of tools like the seL4 microkernel ensured that critical components were isolated, protecting the system even when unverified components were present. By employing rigorous mathematical verification techniques, the program designed software that was both secure and functional.

The HACMS program demonstrated its success through rigorous security testing at each phase. Independent penetration testers, referred to as the “Red Team,” attempted to exploit vulnerabilities in the systems with unrestricted access to documentation and source code. In Phase 1, the Red Team failed to hack into the SMACCMCopter, even with six weeks to discover and exploit potential vulnerabilities. Phase 2 introduced a multi-processor architecture with verified and unverified partitions managed by the seL4 microkernel. Despite granting the Red Team root access to the unverified partition, they were unable to disrupt critical functionality or compromise the system. These results highlighted the effectiveness of HACMS's formal methods in creating software systems that resisted advanced attack scenarios.

The HACMS program not only succeeded in securing its experimental platforms but also extended its methods and tools to other systems, demonstrating their broad applicability. In Phase 3, researchers developed advanced features like geofencing for the SMACCMCopter and adapted HACMS techniques for use in military ground robots, autonomous vehicles, and networked weapon systems. These advancements showcased the program's potential to enhance the cybersecurity of both military and civilian technologies. The verified systems achieved during the HACMS program provide a blueprint for developing high-assurance software across a wide range of critical applications, addressing modern cybersecurity challenges with rigorous, mathematically validated solutions.

Challenges and Future Directions
================================

Lessons Learned
---------------

- Avoid Verifying Existing Code Artifacts
    - Verifying existing systems is more challenging than co-developing a system alongside its correctness proof.
    - Verification experts must decipher required properties from complex codebases and documentation.
    - Systems co-developed with proofs allow developers to make choices that facilitate easier verification.
- Focus on Critical Code
    - Only verify the parts of the system whose correctness is essential for security.
    - Partitioning systems into critical and non-critical code can simplify verification efforts.
    - For example, leveraging the seL4 microkernel enabled the HACMS Air Team to sandbox unverified code securely.
- Eliminate Obvious Bugs First
    - Use low-cost testing tools to remove straightforward bugs before formal verification.
    - This reduces the verification effort by focusing on unusual corner cases.
    - Verification tools are more efficient when systems are pre-screened for common issues.
- Leverage Automation
    - Use decision procedures such as SAT and SMT solvers or tactic libraries to automate portions of the verification process.
    - Automation facilitates updating proofs when system changes occur.
    - Expanding automation capabilities and improving tactic libraries are ongoing research goals.
- Adopt Domain-Specific Languages (DSLs)
    - Write code in DSLs designed to support verification, which simplifies proof generation.
    - DSLs can simultaneously produce executable code and associated proof scripts.
    - These languages reduce complexity and improve the integration of proofs into system development.

Research Challenges
-------------------

Despite the promise of formal methods for building secure and reliable systems, several challenges remain. Developing and validating models of real-world systems, such as the x86 architecture or POSIX interfaces, is labor-intensive, and flaws in these models can undermine the validity of proofs. Increasing automation in tools like SAT and SMT solvers and improving scalability through proof engineering are essential for handling larger systems and managing complex proofs. Integration into standard development workflows is necessary to ensure widespread adoption, as demonstrated by tools like Facebook's INFER. Encouraging developer buy-in often requires reframing formal methods in practical terms, as seen at Amazon Web Services. Additionally, addressing the computational challenges of concurrency is critical, as current techniques struggle with the combinatorial complexity introduced by multi-threaded executions.

Conclusion
==========

The HACMS program demonstrates that formal methods can produce practical, high-assurance systems capable of resisting sophisticated cyber-attacks. It provides a framework for adopting formal methods in broader contexts, emphasizing the need for continued research to enhance scalability, automation, and integration into conventional development practices.