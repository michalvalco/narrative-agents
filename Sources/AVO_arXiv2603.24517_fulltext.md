AVO: Agentic Variation Operators for
Autonomous Evolutionary Search
TerryChen∗,ZhifanYe∗,BingXu∗,ZihaoYe,TimmyLiu,AliHassani,TianqiChen
AndrewKerr,HaichengWu,YangXu,Yu-JungChen,HanfengChen,AdityaKane
RonnyKrashinsky,Ming-YuLiu,VinodGrover,LuisCeze,RogerBringmann,
JohnTran,WeiLiu,FungXie,MichaelLightstone,HumphreyShi
NVIDIA
Abstract
Agentic Variation Operators (AVO) are a new family of evolutionary variation
operatorsthatreplacethefixedmutation,crossover,andhand-designedheuristics
of classical evolutionary search with autonomous coding agents. Rather than
confiningalanguagemodeltocandidategenerationwithinaprescribedpipeline,
AVO instantiates variation as a self-directed agent loop that can consult the
current lineage, a domain-specific knowledge base, and execution feedback to
propose,repair,critique,andverifyimplementationedits. WeevaluateAVOon
attention,amongthemostaggressivelyoptimizedkerneltargetsinAI,onNVIDIA
Blackwell (B200) GPUs. Over 7 days of continuous autonomous evolution on
multi-head attention, AVO discovers kernels that outperform cuDNN by up to
3.5%andFlashAttention-4byupto10.5%acrosstheevaluatedconfigurations.
Thediscoveredoptimizationstransferreadilytogrouped-queryattention,requiring
only30minutesofadditionalautonomousadaptationandyieldinggainsofupto
7.0%overcuDNNand9.3%overFlashAttention-4. Together,theseresultsshow
thatagenticvariationoperatorsmovebeyondpriorLLM-in-the-loopevolutionary
pipelinesbyelevatingtheagentfromcandidategeneratortovariationoperator,and
candiscoverperformance-criticalmicro-architecturaloptimizationsthatproduce
kernelssurpassingstate-of-the-artexpert-engineeredattentionimplementationson
today’smostadvancedGPUhardware.
1 Introduction
Large language models have emerged as powerful components in evolutionary search, replacing
hand-craftedmutationoperators[1]withlearnedcodegeneration[2–5]. Inthesesystems,anLLM
generatescandidatesolutionsconditionedonselectedparents,whileasurroundingframework,which
isusuallyheuristic-based,handlesparentsampling,evaluation,andpopulationmanagement. This
combinationhasproducednotableresultsinmathematicaloptimizationandalgorithmdiscovery,
includingflagshipsystemssuchasFunSearchandAlphaEvolve[3,4]. However,confiningtheLLM
tocandidategenerationwithinaprescribedpipelinefundamentallylimitswhattheLLMcandiscover:
itproducesasingleoutputperinvocation,withnoabilitytoproactivelyconsultreferencematerials,
testitschanges,interpretfeedback,orreviseitsapproachbeforecommittingacandidate. Forthe
mostaggressivelyhand-tunedimplementations,wherefurtherimprovementrequiresdeep,iterative
engineering,thisconstraintisespeciallylimiting.
Westudythisprobleminthecontextofattention[6],thecentraloperationinTransformerarchitectures,
andoneofthemostheavilyoptimizedGPUkernels.TheFlashAttentionlineage[7–10]andNVIDIA’s
cuDNNlibrary[11]havepushedattentionthroughputprogressivelyclosertohardwarelimitsacross
∗EqualContribution
Preprint.
6202
raM
52
]GL.sc[
1v71542.3062:viXra

EVO: Classical Evolutionary Search Frameworks AVO: Agentic Variation Operators
Agent Loop: Planning, Implementing,
Single-Turn or
Testing, Debugging
Predefined Workflow
Previous Evaluation
AI Agent
Previous Sampling LLM Evaluation Solutions Utility
Solutions Tools Memory
Figure1: EVOvsAVO:Comparisonbetweenpriorevolutionarysearchframeworks(e.g. FunSearch,
AlphaEvolve, and related LLM-augmented evolutionary approaches) and the proposed Agentic
VariationOperator. Left: PriorapproachesfollowafixedpipelinewheretheLLMisconfinedtoa
single-turngenerationsteporapredefinedworkflow,withsamplingandevaluationcontrolledbythe
framework. Right: AVOreplacesthispipelinewithanautonomousAIagentthatiterativelyplans,
implements,tests,anddebugsacrosslong-runningsessions,withdirectaccesstoprevioussolutions,
evaluationutilities,tools,andpersistentmemory.
successiveGPUgenerations, withbothFlashAttention-4(FA4)andcuDNNrequiringmonthsof
manualoptimizationonthelatestBlackwellarchitecture. Surpassingtheseimplementationsdemands
sustained,iterativeinteractionwiththedevelopmentenvironment: studyinghardwaredocumentation,
analyzingprofileroutputtoidentifybottlenecks,implementingandtestingcandidateoptimizations,
diagnosingcorrectnessfailures,andrevisingstrategybasedonaccumulatedexperience.
Recentprogressindeepagents[12–16]demonstratesthatLLMsaugmentedwithplanning,persistent
memory,andtoolusecanautonomouslynavigatesuchmulti-stepengineeringworkflows,withappli-
cationsrangingfromresolvingcomplexGitHubissuestogeneratingkeydeeplearningsoftware[17].
ThismotivatesafundamentallydifferentroleforLLMsinevolutionarysearch: ratherthanconfining
themwithinafixedpipeline,wecanelevateadeepagenttoserveasthevariationoperatoritself. To
thisend,weproposeAgenticVariationOperators(AVO),inwhichaself-directedcodingagent
replacesthemutationandcrossoverprocessinpreviousworksbasedonsingle-turnLLMs[3–5]or
fixedworkflows[18]. TheAVOagenthasaccesstoallpriorsolutions,adomain-specificknowledge
base,andtheevaluationutility. Itautonomouslydecideswhattoconsult,whattoedit,andwhento
evaluate,enablingcontinuousimprovementsoverextendedtimehorizons.
To demonstrate its effectiveness, we apply AVO to multi-head attention (MHA) kernels on the
BlackwellB200GPU,anddirectlycompareagainsttheexpert-optimizedcuDNNandFlashAttention-
4kernels. Over7daysofcontinuousevolutionwithouthumanintervention,theagentexploredover
500optimizationdirectionsandevolved40kernelversions,producingMHAkernelsachievingup
to1668TFLOPSatBF16precision, outperformingcuDNNbyupto3.5%andFlashAttention-4
by up to 10.5%. Our analysis of agent-discovered optimizations reveals that they span multiple
levelsofkerneldesign,includingregisterallocation,instructionpipelinescheduling,andworkload
distribution,reflectinggenuinehardware-levelreasoning. Empirically,wefindthattheoptimization
techniquesdiscoveredonMHAtransfereffectivelytogrouped-queryattention(GQA):adaptingthe
evolvedMHAkerneltosupportGQArequiresonly30minutesofadditionalautonomousagenteffort,
yieldingupto7.0%performanceimprovementovercuDNNand9.3%overFlashAttention-4.
Ourcontributionsareasfollows:
• WeintroduceAgenticVariationOperators(AVO),anewfamilyofevolutionaryvariation
operatorsthatelevatetheagentfromcandidategeneratortovariationoperator,autonomously
exploringdomainknowledge,implementingedits,andvalidatingresultsthroughiterative
interactionwiththeenvironment.
• Weachievestate-of-the-artMHAthroughputonNVIDIAB200GPUsacrossthebench-
marked configurations, reaching up to 1668 TFLOPS and outperforming cuDNN by up
to3.5%andFlashAttention-4byupto10.5%. Furthermore,weshowthatthediscovered
optimizationsreadilytransfertoGQA,requiringonly30minutesofautonomousadaptation
andyieldinggainsofupto7.0%overcuDNNand9.3%overFlashAttention-4.
2

• Weprovideadetailedanalysisofthemicro-architecturaloptimizationsdiscoveredbythe
agentunderthebenchmarkedsettings,showingtheagentperformsgenuinehardware-level
reasoningratherthansuperficialcodetransformations.
2 Background
2.1 EvolutionarySearchandVariationOperators
EvolutionarysearchoptimizesoveraspaceofcandidatesbymaintainingapopulationPanditeratively
expandingitwithnewsolutions[19]. Apopulationisasetofsolution-scorepairsP ={(x ,f(x ))},
i i
wheref isascoringfunctionthatevaluateseachcandidatesolution. Eachiterationproducesanew
candidatex andupdatesthepopulation:
t+1
(cid:0) (cid:1)
P =UpdateP , (x , f(x )) , x =Vary(P ), (1)
t+1 t t+1 t+1 t+1 t
where Update adds the new solution to the population, possibly pruning low-score members to
maintainaboundedarchive. WecallVarythevariationoperator: themechanismbywhichnew
candidatesareproducedfromexistingones. InworkssuchasFunSearch[3],AlphaEvolve[4],and
relatedLLM-augmentedevolutionarymethods[2,20,5],thevariationoperatordecomposesintotwo
stages:
(cid:0) (cid:1)
Vary(P )=GenerateSample(P ) , (2)
t t
whereSampleselectsoneormoreparentsolutionsfromP (typicallyguidedbyscore-basedand
t
diversity-basedheuristics),andGenerateproducesanewcandidateconditionedonthesampled
parents.
LLM-augmentedvariation. Intheseapproaches,GenerateisimplementedbyanLLMthatis
promptedwiththesampledparentsandaskedtoproduceamoreoptimizedsolution. TheSample
step, however, remains a fixed algorithmic procedure: AlphaEvolve maintains an island-based
evolutionary database inspired by MAP-Elites [21], where a prompt sampler selects parent and
inspirationprogramsusingpredefinedfitness-basedanddiversity-basedheuristics. LoongFlow[18]
similarlyreliesonaMAP-ElitesarchivewithBoltzmannselectionforSample,whilestructuring
Generate as a fixed Plan-Execute-Summarize pipeline where the LLM sequentially generates a
modificationplan,producesthecode,andsummarizesinsights. Inalltheseapproaches,theLLM
onlyparticipatesinGenerate: thesamplingstrategy,evaluationprotocol,populationmanagement,
andtheorderofoperationsarealldeterminedbytheframework,notbytheLLM.
Learnedvariation. TTT-Discover[22]goesfurtherbyupdatingtheLLMpolicyitselfthrough
test-timegradientupdates,enablingthemodeltolearnanimprovedGenerateduringthesearch.
Nevertheless,Sampleremainsafixedalgorithm: aPUCT-basedselectionrule[23]determineswhich
statestoexpand,andabuffermanagesthepopulationwithpredeterminedupdaterules. Evenwitha
learnedGenerate,theLLM’sroleisstillconfinedtocandidategenerationwithinarigidalgorithmic
structurethatprescribeswhenandhowitisinvoked.
Incontrast,theagenticvariationoperatorweintroduceinSection3replacestheentireVarywith
aself-directedagentthatsubsumesSample,Generate,andevaluationintoasingleautonomous
loop. TheagenthasfullagencyoverwhentoconsultreferencematerialsandpastsolutionsP ,what
t
diagnosticteststorun,andhowtoreviseitsoptimizationstrategy.
AVOisorthogonaltothechoiceofpopulationstructure: theagenticoperatorcaninprinciplebeused
withinarchive-based,island-based,orsingle-lineageevolutionaryregimes. Inthispaperwestudythe
single-lineagesettingtoisolatetheeffectoftheoperatoritself.
2.2 AttentionKernelsonModernGPUs
Attention computation. Given query, key, and value matrices Q, K, V, attention computes
√
O =softmax(QK⊤/ d)V,wheredistheheaddimension. Anaiveimplementationmaterializes
thefullN ×N scorematrixS =QK⊤,makingtheoperationmemory-boundforlargesequence
lengthsN. TheFlashAttentionalgorithm[7]avoidsthisbycomputingattentionintiles: itprocesses
keyblockssequentially,maintainingarunningsoftmax(withrunningrow-maximumandrow-sum)
andaccumulatingtheoutputOincrementally. Thistilingeliminatestheneedtostorethefullscore
matrix,shiftingthebottleneckfrommemorybandwidthtocomputethroughputonmodernGPUs.
3

| Input to AVO |     |     | AVO Main Agent Loop |     |     |     |     |          |      |
| ------------ | --- | --- | ------------------- | --- | --- | --- | --- | -------- | ---- |
|              |     |     |                     |     |     |     |     | Monitor  | AVO  |
Population	𝒫! Knowledge Base 𝒦 Planning Implementation Stagnation Supervisor
|        | CUDA & PTX  |     | Propose Edits  |     |     | Apply Code    |     |     | Agent |
| ------ | ----------- | --- | -------------- | --- | --- | ------------- | --- | --- | ----- |
| 𝑥!,𝐟𝑥! | Documents   |     | (using 𝒦 & 𝒫!) |     |     | Modifications |     |     |       |
R e fe r e n c e  G P U
|     | Ke r n e l  C o d eb | a s es |     |     |     | Conditional Intervention |     |     |     |
| --- | -------------------- | ------ | --- | --- | --- | ------------------------ | --- | --- | --- |
𝒫#, 𝒦, 𝐟
…
| 𝑥",𝐟𝑥" |                     |     |     | AI Agent |        |     |     |     |     |
| ------ | ------------------- | --- | --- | -------- | ------ | --- | --- | --- | --- |
|        | Scoring Function 𝐟  |     |     | Tools    | Memory |     |     |     |     |
… …
|        |                   |            | Bug-Fixing                  | Reasoning |     | Evaluation      |               | Output of AVO |            |
| ------ | ----------------- | ---------- | --------------------------- | --------- | --- | --------------- | ------------- | ------------- | ---------- |
|        |                   |            | D ia g n os e ,  R ep a ir, |           |     | Evalua t e  P e | rf o r m ance |               |            |
| 𝑥#,𝐟𝑥# | Correctness       | Throughput |                             |           |     |                 |               |               |            |
|        | Check Measurement |            | a n d  A d a p t P la n     |           |     | ( U s in        | g   𝐟 )       |               | 𝑥#$!,𝐟𝑥#$! |
Figure2: IllustrationoftheAgenticVariationOperator(AVO).
AttentionkernelonBlackwellhardware. OnNVIDIA’sBlackwellarchitecture,state-of-the-art
attention kernels such as FA4 [10] employ warp specialization: different warp groups within a
threadblockareassigneddistinctrolesintheattentionpipeline. MMAwarpsexecutethetwocore
matrixmultiplicationsviaBlackwell’stensorcoreinstructions: theQKGEMM(producingscores
S)andthePVGEMM(multiplyingthesoftmaxoutputP = softmax(S)byV toaccumulatethe
output O). Softmax warps compute attention weights P from the scores S, applying the online
softmaxalgorithmwitharunningrow-maximum. CorrectionwarpsrescaletheoutputaccumulatorO
whentherunningmaximumchangesacrossK-blockiterations(arequirementoftheonlinesoftmax
algorithm). LoadandepiloguewarpshandledatamovementviatheTensorMemoryAccelerator
(TMA). In FA4’s pipeline, these groups operate concurrently across two Q-tiles (a dual Q-stage
design), withbarrier-basedsignalingtocoordinatehandoffs. Forcausalattention, someK-block
iterations are fully masked (no valid attention entries) and others are fully unmasked, leading to
differentexecutionpathswithinthesamekernel. WithFA4alreadyrepresentingahighlyoptimized
design, furtherimprovementsdemanddeephardwareexpertise, broadexplorationacrossdiverse
optimizationstrategies,andrepetitivedebuggingandprofiling.
3 AgenticVariationOperators
AVOconsolidatesthesampling,generation,andevaluationstagesofevolutionarysearchintoasingle
autonomousagentrun,eliminatingtherigidpipelinethatconstrainsexistingapproaches. Belowwe
formalizethisoperator,detailwhatoccurswithinasinglevariationstep,anddescribethemechanism
thatenablesmulti-dayautonomousexploration.
3.1 Formulation
Previousevolutionarysearchapproaches[3,4]decomposethevariationoperatoras:
|     |     | Vary(P | )=Generate(Sample(P |     |     | )), |     |     | (3) |
| --- | --- | ------ | ------------------- | --- | --- | --- | --- | --- | --- |
|     |     |        | t                   |     | t   |     |     |     |     |
confiningtheLLMtotheGeneratestepwithinafixedpipeline. AsillustratedinFigure2,AVO
replacesthisdecompositionwithasingleautonomousagentrun:
|     |     |     | Vary(P )=Agent(P | ,K,f), |     |     |     |     | (4) |
| --- | --- | --- | ---------------- | ------ | --- | --- | --- | --- | --- |
|     |     |     | t                | t      |     |     |     |     |     |
whereP = {(x ,f(x )),...,(x ,f(x ))}isthefulllineageofsolutionsandtheirscores, K isa
| t                                 | 1 1 |     | t t                   |     |     |     |     |     |     |
| --------------------------------- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- |
| domain-specificknowledgebase,andf |     |     | isthescoringfunction. |     |     |     |     |     |     |
Inoursetting,eachx isaCUDAkernelimplementation(sourcecodewithinlinePTX),andf evalu-
i
atesacandidatealongtwodimensions:numericalcorrectnessagainstareferenceimplementation,and
throughputinTFLOPSonthetargethardware. Inpractice,f(x )=(f (x ),f (x ),...,f (x ))is
|     |     |     |     |     | i   | 1   | i 2 | i   | n i |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ann-dimensionalvectorandf representsthescorefortestconfigurationj. Acandidatex thatfails
|     |     | j   |     |     |     |     |     |     | i   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
correctnessisassignedzeroscore(i.e.,f j (x i )=0)regardlessofthroughput. TheknowledgebaseK
containsCUDAprogrammingguides,PTXISAdocumentation,Blackwellarchitecturespecifications,
andexistingkernelimplementationsincludingFlashAttention-4sourcecode.
AVO defines a family of agentic variation operators for evolutionary search. In this work, we
instantiateAVOinasingle-lineageautonomousrunstartingfromaseedprogramx ,producinga
0
4

sequenceofcommittedimprovementsx ,x ,...,x . TheaccumulatedlineageP servesascontext
1 2 t t
forsubsequentvariationsteps.
3.2 AnatomyofaVariationStep
AsinglevariationstepinAVO,producingx fromthecurrentlineageP ,isanautonomousagent
t+1 t
loop. Theagentisageneral-purposecodingagentwithplanning,tooluse,andpersistentmemory
(detailsinSection4),andasinglestepmayinvolvenumerousinternalactions.
WeobservethattheagentfrequentlyexaminesmultiplepriorimplementationsinP withinasingle
t
variationstep,comparingtheirprofilingcharacteristicstoidentifybottlenecksandopportunities,and
consultingdocumentationinKtounderstandtherelevanthardwareconstraintsbeforeimplementinga
candidateoptimization. Theagenttheninvokesf totesttheresult. Whenacandidatefailscorrectness
checksorfailstoimproveonthecurrentbenchmarksuite,theagentdiagnosestheissueandrevises
itsapproach,repeatingthisedit-evaluate-diagnosecycleuntilitcommitsasatisfactoryx . This
t+1
designallowstheagenttoadaptitsoptimizationstrategyasthesearchprogresses: earlystepsmay
focusonstructuralchangesinformedbyreferenceimplementationsinK,whilelaterstepscanshift
towardmicro-architecturaltuningguidedbyprofilingfeedbackfromf andpatternsobservedacross
theaccumulatedlineageP .
t
Inourcurrentimplementation,wepersistanewcommittedversiononlywhenitpassescorrectness
checksandmatchesorimprovesthebenchmarkscorerelativetothebestcommittedversionsofar;
unsuccessfulintermediateattemptsremainpartoftheagent’sinternalsearchtrajectorybutarenot
addedtothecommittedlineage.
3.3 ContinuousEvolution
AlthoughAVOisdefinedatthelevelofvariationoperatorsforevolutionarysearch,thepresentstudy
evaluatesasingle-lineagecontinuousinstantiation,leavingpopulation-levelbranchingandarchive
managementtofutureextensions. TheAVOagentoperatesasacontinuousloopthatperiodically
producesnewsolutionswithouthumanintervention. Eachcommittedversionx ispersistedasagit
i
commitalongwithitsscore,maintainingfullstatecontinuityacrosstheentireevolutionaryprocess.
Inlong-runningautonomousoptimization,twofailuremodescanimpedeprogress: theagentmay
stallwhenitexhaustsitscurrentlineofexploration,oritmayenterunproductivecyclesofeditsthat
repeatedlyfailtoimprovescores. Tomitigateboth,AVOincorporatesaself-supervisionmechanism
that detects these scenarios and intervenes. Once triggered, the mechanism reviews the overall
evolutionarytrajectoryandsteersthesearchtowardseveralcandidateoptimizationdirections. This
conditionalinterventioneffectivelyredirectsexplorationwithfreshperspectivewhenthecurrent
strategyhasplateaued.
The7-dayrunthatproducedourfinalmulti-headattentionkernelspanned40successiveversions.
Throughoutthisprocess,themainagentautonomouslydecidedwhentoattemptnewoptimizations,
whentorevisitearlierapproachesinP ,andwhentoshiftstrategy,whilethesupervisormaintained
t
forwardprogressbyinterveningduringperiodsofstagnation.
4 Experiments
4.1 Setup
Agent. Weuseaninternally-developedgeneral-purposecodingagentpoweredbyfrontierLLMsas
theAVOvariationoperator. Theagenthasaccesstostandardsoftwareengineeringtools,including
autonomous code editing, shell command execution, file system navigation, and documentation
retrieval. Itmaintainspersistentmemorythroughitsconversationhistory,whichaccumulatesthe
fullcontextofprioredits,compileroutputs,profilingresults,andreasoningacrosstheevolutionary
process. Notask-specificmodificationsaremadetotheagentforkerneloptimization;thesameagent
usedforgeneralsoftwareengineeringtasksisdeployedhere,withthedomain-specificknowledge
baseKandscoringfunctionf providedtotheagentasdescribedinSection3.1.
Hardwareandsoftware. FollowingthesetupofFA4[10],allofourexperimentsareconductedon
NVIDIAB200GPUswithCUDA13.1andPyTorch2.10.0.
5

Forward TFLOPS on B200 (causal=False) Forward TFLOPS on B200 (causal=True)
| 1800 cuDNN   |                   | 1800 cuDNN |     |      |      |
| ------------ | ----------------- | ---------- | --- | ---- | ---- |
| FA4          |                   | FA4        |     |      |      |
| 1700 AVO     | 1664 163816511668 | 1700 AVO   |     |      |      |
| 160916141615 | 16261637          |            |     |      | 1637 |
| 157315781573 |                   |            |     | 1582 | 1590 |
| 1600         |                   | 1600       |     | 1551 | 1550 |
1502
| SPOLFT 1500 |     | SPOLFT 1500 | 1477 1482 |     |     |
| ----------- | --- | ----------- | --------- | --- | --- |
1412
| 1400 |     | 1400 1392 |     |     |     |
| ---- | --- | --------- | --- | --- | --- |
1344
| 1300          |               | 1300 1259 |        |        |        |
| ------------- | ------------- | --------- | ------ | ------ | ------ |
| 1200          |               | 1200      |        |        |        |
| 1100          |               | 1100      |        |        |        |
| 1000          |               | 1000      |        |        |        |
| 4K 8K         | 16K 32K       | 4K        | 8K     | 16K    | 32K    |
| (bs=8) (bs=4) | (bs=2) (bs=1) | (bs=8)    | (bs=4) | (bs=2) | (bs=1) |
Figure3: Multi-headattentionforward-passprefillingthroughput(TFLOPS)onNVIDIAB200with
headdimension128,16heads,andBF16precision. Batchsizeandsequencelengtharevariedwitha
fixedtotalof32ktokens.
Baselines. Wecompareagainsttwostate-of-the-artbaselines:(1)cuDNN:NVIDIA’sclosed-source
attentionkernel,measuredusingcuDNNversion9.19.1,whichincludescustomoptimizationsfor
Blackwell;and(2)FlashAttention-4(FA4)[10]: thelatestopen-sourceattentionkerneloptimized
forBlackwell,measuredusingtheofficialimplementation(commit71bf77c).
Benchmark Configurations. We evaluate the forward prefilling throughput with head dimen-
sion 128 and BF16 precision across sequence lengths {4096,8192,16384,32768}. Following
FlashAttention-4[10],wecontrolthetotalnumberoftokensto32768byadjustingthebatchsize
foreachsequencelength(e.g.,batchsize8atsequencelength4096,batchsize1atsequencelength
32768). Formulti-headattention(MHA),weuse16headsunderbothcausalandnon-causalmasking.
Forgrouped-queryattention(GQA),weevaluatetwoconfigurationsdrawnfromtheQwen3model
family[24]: 32queryheadswith4KVheads(groupsize8,asinQwen3-30B-A3B)and32query
headswith8KVheads(groupsize4,asinQwen3-8B).Forthroughputmeasurement,weusedthe
sametimingscriptfromtheFA4repository2andthesamenumberofwarm-upandrepeatroundsas
theFA4paper. Inaddition,werantheexperiment10timestoobtaintheaverageperformanceandthe
standarddeviation. Thesamesetupisusedbothforagentevolutionandforbenchmarkingthefinal
evolvedkernelsagainstthebaselines.
4.2 Multi-HeadAttention
Figure3presentsthebenchmarkingresultsforMHA.Oncausalattention,AVOoutperformsboth
baselinesacrossalltestedconfigurations,withgainsrangingfrom+0.4%to+3.5%overcuDNN
and+5.0%to+10.5%overFA4. Onnon-causalattention,AVOachievesmodestgainsatlonger
sequences (+1.8% to +2.4% over cuDNN at sequence lengths larger than 16384) but is within
measurementnoiseofbothbaselinesatshortersequences. InSection4.4,weshowhowtheagent
obtainstheperformancegainsthroughcontinuousevolution.
4.3 Grouped-QueryAttention
Toevaluatewhetheragent-discoveredoptimizationstransferbeyondthebenchmarksettingsusedin
evolution,wepromptedtheAVOagenttoadapttheevolvedMHAkerneltosupportGQA.Theagent
completedthisadaptationautonomouslyinapproximately30minutes,producingaGQA-capable
kernelwithoutanyhumanguidanceontherequiredchanges.
Figure4presentstheresultsacrosstwoGQAconfigurations. AVOoutperformsbothbaselinesacross
allconfigurations. OncausalGQA,AVOachievesupto+7.0%overcuDNNand+9.3%overFA4.
Onnon-causalGQA,gainsreachupto+6.0%overcuDNNand+4.5%overFA4. ThestrongGQA
performancedemonstratesthattheoptimizationsdiscoveredbytheagentduringMHAevolutionare
notspecifictotheMHAconfigurationsusedduringevolution,butgeneralizetothedistinctcompute
andmemoryaccesspatternsofGQA.
2https://github.com/Dao-AILab/flash-attention/blob/main/benchmarks/benchmark_attn.py
6

|        | Forward TFLOPS (Group=8, causal=False) |      |          |      |         | Forward TFLOPS (Group=8, causal=True) |           |      |           |
| ------ | -------------------------------------- | ---- | -------- | ---- | ------- | ------------------------------------- | --------- | ---- | --------- |
| 1900   |                                        |      |          |      | 1900    |                                       |           |      |           |
|        | cuDNN                                  |      |          |      |         | cuDNN                                 |           |      |           |
| 1800   | FA4                                    |      |          |      | 1800    | FA4                                   |           |      |           |
|        | AVO                                    |      | 16431663 |      |         | AVO                                   |           |      |           |
| 1700   |                                        | 1677 |          |      | 1 7 0 0 |                                       |           |      | 1603 1625 |
|        | 1646 16201633                          |      | 1607     |      |         |                                       |           | 1618 |           |
|        | 15901602                               |      |          |      |         |                                       |           | 1571 | 1530      |
| 1600   |                                        |      |          | 1528 | 1 6 0 0 |                                       |           | 1541 |           |
| SPOLFT |                                        |      |          | 1472 | SPOLFT  |                                       | 1503 1511 |      |           |
| 1500   |                                        |      |          | 1441 | 1500    | 1467                                  | 1471      |      |           |
| 1400   |                                        |      |          |      | 1400    | 1377                                  |           |      |           |
1342
| 1300        |                                        |        |           |           | 1300        |                                       |           |        |        |
| ----------- | -------------------------------------- | ------ | --------- | --------- | ----------- | ------------------------------------- | --------- | ------ | ------ |
| 1200        |                                        |        |           |           | 1200        |                                       |           |        |        |
| 1100        |                                        |        |           |           | 1100        |                                       |           |        |        |
| 1000        |                                        |        |           |           | 1000        |                                       |           |        |        |
|             | 4K                                     | 8K     | 16K       | 32K       |             | 4K                                    | 8K        | 16K    | 32K    |
|             | (bs=8)                                 | (bs=4) | (bs=2)    | (bs=1)    |             | (bs=8)                                | (bs=4)    | (bs=2) | (bs=1) |
|             | Forward TFLOPS (Group=4, causal=False) |        |           |           |             | Forward TFLOPS (Group=4, causal=True) |           |        |        |
| 1900        |                                        |        |           |           | 1900        |                                       |           |        |        |
|             | cuDNN                                  |        |           |           |             | cuDNN                                 |           |        |        |
| 1800        | FA4                                    |        |           |           | 1800        | FA4                                   |           |        |        |
|             | AVO                                    |        |           |           |             | AVO                                   |           |        | 1647   |
| 1700        |                                        | 1673   | 1626 1679 |           | 1700        |                                       |           |        |        |
|             | 1633 16171627                          |        | 1624      |           |             |                                       |           |        | 1601   |
|             | 15861601                               |        |           |           |             |                                       |           | 1603   |        |
| 1600        |                                        |        |           |           | 1600        |                                       |           | 1568   | 1517   |
|             |                                        |        |           | 1477 1526 |             |                                       | 1497 1506 | 1536   |        |
| SPOLFT 1500 |                                        |        |           | 1460      | SPOLFT 1500 | 1464                                  | 1470      |        |        |
| 1400        |                                        |        |           |           | 1400        | 13681344                              |           |        |        |
| 1300        |                                        |        |           |           | 1300        |                                       |           |        |        |
| 1200        |                                        |        |           |           | 1200        |                                       |           |        |        |
| 1100        |                                        |        |           |           | 1100        |                                       |           |        |        |
| 1000        |                                        |        |           |           | 1000        |                                       |           |        |        |
|             | 4K                                     | 8K     | 16K       | 32K       |             | 4K                                    | 8K        | 16K    | 32K    |
|             | (bs=8)                                 | (bs=4) | (bs=2)    | (bs=1)    |             | (bs=8)                                | (bs=4)    | (bs=2) | (bs=1) |
Figure4: Grouped-queryattentionforward-passprefillingthroughput(TFLOPS)onNVIDIAB200
with 32 query heads, head dimension 128 and BF16 precision. Results are shown for two GQA
configurations(groupsizes8and4)underbothcausalandnon-causalmasking. TheGQAkernelwas
producedbypromptingtheAVOagenttoadapttheevolvedMHAkernel,requiringapproximately30
minutesofautonomouseffort.
4.4 EvolutionTrajectory
InFigure5andFigure6,weshowtheevolutiontrajectoryofAVOacrossthe40committedkernel
versionsproducedduringthe7-dayevolution. Notethatthesetrajectoriesvisualizethecommitted
sequence,ratherthanthefullinternalsearchtreeexploredbetweenthecommits. Weobservedthe
followingpatterns:
Scale of exploration. The 40 committed versions shown in the trajectory represent only the
successful outcomes of a much larger search. Over the 7-day evolution, the agent explored over
500candidateoptimizationdirectionsinternally,includingattemptsthatfailedcorrectnesschecks,
regressedthroughput,orwereabandonedafterprofiling. Thisvolumeofsystematicexploration,each
directionrequiringreadingdocumentation,implementingchanges,compiling,testing,andprofiling,
farexceedswhatahumanengineercouldaccomplishinthesametimeframe.
Discretejumpsratherthangradualimprovement. Throughputimprovesindistinctstepssep-
arated by plateaus where successive versions refine implementation details without measurably
changingperformance. Thefivelargestgainscorrespondtoarchitecturalinflectionpoints: theintro-
ductionofQK-PVinterleavingwithbitmaskcausalmasking(version8),arestructuredsingle-pass
softmaxcomputation(version13),thebranchlessaccumulatorrescalingwithalightermemoryfence
forunmaskediterations(version20),thecorrection/MMApipelineoverlap(version30),andregister
rebalancingacrosswarpgroups(version33). Wediscusssomeoftherepresentativeoptimizations
in Section 5. The remaining versions contribute individually smaller but collectively substantial
micro-architecturalrefinements.
Diminishingreturns. Theearlierversions(v1throughv20)deliverthelargestabsolutegainsper
version, closing the gap between a naive implementation and the well-optimized baselines. The
laterversions(v21throughv40)yieldsmallerbutcompoundingimprovementsthroughcycle-level
schedulingandrefinedresourceallocation. Thispatternisconsistentwiththegeneralobservation
7

1600
1500
1400
1300
1200
1100
v1v2v3v4v5v6v7v8v9 v10 v11 v12 v13 v14 v15 v16 v17 v18 v19 v20 v21 v22 v23 v24 v25 v26 v27 v28 v29 v30 v31 v32 v33 v34 v35 v36 v37 v38 v39 v40
Kernel Version
SPOLFT
Evolution Trajectory of AVO on Causal BF16 Multi-head Attention
AVO v40 (1520 TFLOPs)
cuDNN
1488
FA4
1426
New best (Geomean) seq_len=16k cuDNN (1488)
Running best (Geomean) seq_len=8k FA4 (1426)
seq_len=32k seq_len=4k
Figure5: EvolutiontrajectoryofAVOacross40kernelversionsover7daysoncausalMHA.The
solidgreenlinetrackstherunning-bestgeometricmeanthroughputacrossallconfigurations;green
circlesmarkversionsthatsetanewbest. Dashedcoloredlinesshowper-configurationthroughput
(seq_len=4k,8k,16k,32k). Horizontaldashedlinesindicatethegeometricmeanthroughputof
cuDNNandFA4.
1700
1650
1600
1550
1500
1450
1400
1350
1300
v1v2v3v4v5v6v7v8v9 v10 v11 v12 v13 v14 v15 v16 v17 v18 v19 v20 v21 v22 v23 v24 v25 v26 v27 v28 v29 v30 v31 v32 v33 v34 v35 v36 v37 v38 v39 v40
Kernel version
SPOLFT
Evolution Trajectory of AVO on Non-Causal BF16 Multi-head Attention
FA4 AVO v40 (1630 TFLOPs)
1620
cuDNN
1611
New best seq_len=16k cuDNN (1611)
Running best seq_len=8k FA4 (1620)
seq_len=32k seq_len=4k
Figure6:EvolutiontrajectoryofAVOacross40kernelversionsover7daysonnon-causalMHA.The
solidgreenlinetrackstherunning-bestgeometricmeanthroughputacrossallconfigurations;green
circlesmarkversionsthatsetanewbest. Dashedcoloredlinesshowper-configurationthroughput
(seq_len=4k,8k,16k,32k). Horizontaldashedlinesindicatethegeometricmeanthroughputof
cuDNNandFA4.
thatearlykerneldevelopmentcapturescoarse-grainedgainswhilelate-stageoptimizationsqueezes
outremainingheadroomthroughincreasinglyfine-grainedtuning.
5 AnalysisofAgent-DiscoveredOptimizations
The40-versionAVOevolutionproducedmulti-leveloptimizationsthatindividuallyyieldmeasurable
throughputgainsandcollectivelyaccountfortheimprovementsreportedinSection4. Weexamine
threerepresentativeoptimizationstoillustratethenatureanddepthoftheagent’shardwarereasoning.
Foreach,wedescribethebottlenecktheagentidentifiedinitsownkernel,thechangeitmade,andits
measuredimpact(ablationbetweentheversionimmediatelybeforeandafter). Table1providesa
summary.
8

Table1: Summaryofagent-discoveredoptimizationsandtheirmeasuredablationgains(geomean
TFLOPSimprovementovertheprecedingversion,acrossallbenchmarkconfigurations).
Optimization Versions Non-causal Causal
Branchlessaccumulatorrescaling v19→v20 +8.1% +1.6%
Correction/MMApipelineoverlap v29→v30 +1.1% +0.4%
Registerrebalancingacrosswarpgroups v32→v33 +2.1% ∼0%
5.1 BranchlessAccumulatorRescaling
Bottleneck. Intheonlinesoftmaxalgorithm,therunningrow-maximummaychangeasnewkey
blocks are processed. When it does, the output accumulator O must be rescaled to account for
the updated maximum. In version 19 of the AVO kernel, this rescaling was implemented with a
conditionalbranch: thekernelfirstcheckedwhetheranythreadinthewarprequiredrescaling,and
skippedtheoperationentirelywhenthemaximumwasunchanged. Whilethisavoidsunnecessary
computation,thebranchintroduceswarpsynchronizationoverheadoneveryiterationofthekey-block
loop(seeSection2.2),andtheconditionalcontrolflowpreventstheuseoflightermemoryfencesin
thecorrectionpath.
AVO’s approach. In version 20, the agent replaced the conditional branch with a branchless
speculative path. The rescale factor is always computed, and a predicated select substitutes 1.0
whenrescalingisunnecessary;thecostofanunnecessarymultiply-by-oneisnegligiblecompared
to the synchronization overhead it replaces. By eliminating the branch, the agent also removed
warpdivergenceinthecorrectionpath,whichinturnallowedittoreplaceablockingmemoryfence
(whichstallsuntilallpendingmemorywritescomplete)withalighternon-blockingfencethatmerely
enforces ordering. The non-blocking fence is safe here because the branchless path guarantees
thatallthreadsinthewarpfollowthesamecontrolflow,ensuringreconvergencebeforethenext
synchronizationpoint.
Measuredimpact. Thecombinedeffectofbranchlessrescalingandthelighterfenceyields+8.1%
geomeanthroughputonnon-causaland+1.6%oncausalattention,thelargestsingleoptimization
intheevolution. Theasymmetryarisesbecausethebranchlesspathappliesonlytofullyunmasked
iterationsofthekey-blockloop:non-causalattentionprocessesallkeyblockswithoutmasking,while
causalattentionretainstheoriginalbranchedlogicformaskedkeyblocks.
5.2 Correction/MMAPipelineOverlap
Bottleneck. The attention pipeline processes two Q-tiles concurrently (dual Q-stage; see Sec-
tion2.2),eachrequiringaPVGEMMfollowedbyoutputnormalizationbythecorrectionwarp. In
version29oftheAVOkernel,thetwostageswereserializedattheMMA-to-correctionboundary:
thecorrectionwarphadtowaitforbothPVGEMMstocompletebeforeitcouldbeginnormalizing
eitherstage’soutput,leavingitidlethroughoutthesecondGEMM.
AVO’sapproach. Inversion30,theagentrestructuredthepipelinetoallowthecorrectionwarp
tobeginnormalizingthefirststage’soutputassoonasitsPVGEMMcompletes,overlappingthis
workwiththesecondstage’sPVGEMM.Thisconvertsasequentialdependencyintoapipelined
execution,reducingtheidletimeonthecorrectionwarp.
Measuredimpact. Thispipelinerestructuringyields+1.1%geomeanthroughputonnon-causal
and+0.4%oncausalattention.
5.3 RegisterRebalancingAcrossWarpGroups
Bottleneck. Blackwellpartitionsafixedbudgetof2048warp-registersperSMacrosswarpgroups.
Inversion32oftheAVOkernel,theallocationfollowedthepatternofFlashAttention-4[10]: 192
registersforthe8softmaxwarps,80forthe4correctionwarps,and48fortheremaining4warps.
Profilingrevealedthatthecorrectionwarpgroupwasspillingvaluestoslowerlocalmemorydueto
itslimited80-registerbudget,whilethesoftmaxgrouphadsubstantialheadroom.
9

AVO’sapproach. Inversion33,theagentredistributed8registersfromthesoftmaxgrouptoeach
of the other two groups, arriving at a 184/88/56 allocation. This redistribution is viable because
theAVOkernel’ssoftmaximplementationprocessesscorevaluesinsmallfragmentswithpacked
arithmetic,resultinginalowpeakregisterusagethatleavesampleheadroomevenat184registers.
The correction warp group benefits from the additional registers because, following the pipeline
overlapoptimization(Section5.2),itrunsconcurrentlywiththesecondPVGEMMandisonthe
executioncriticalpath. With88ratherthan80registers,feweroutputvaluesspilltolocalmemory,
reducingstalls.
Measuredimpact. Registerrebalancingyields+2.1%geomeanthroughputonnon-causaland
approximately0%oncausalattention.
5.4 Discussion
What is notable about these optimizations is that each requires jointly reasoning about multiple
hardwaresubsystems, includingsynchronizationandmemoryordering, pipelinescheduling, and
register allocation, rather than tuning any single parameter in isolation. This depth of reasoning,
carriedoutautonomouslythroughiterativeinteractionwithdocumentationandprofilingfeedback,
suggeststhatagenticvariationoperatorscanserveasaneffectivemechanismforexpert-levelkernel
optimization.
6 Conclusion
WeintroducedAgenticVariationOperators(AVO),anewfamilyofevolutionaryvariationoperators
that elevate the agent from candidate generator to variation operator. Applied to forward-pass
attentiononNVIDIABlackwellGPUs,AVOproduceskernelssurpassingcuDNNbyupto3.5%
andFlashAttention-4byupto10.5%over7daysofcontinuousautonomousevolution. Furthermore,
we show that the discovered optimizations transfer readily to grouped-query attention, requiring
only30minutesofadditionalautonomousadaptation. Together,theseresultsdemonstratethatAVO
candiscoverperformance-criticalmicro-architecturaloptimizationsthatproducekernelssurpassing
state-of-the-artexpert-engineeredimplementations. BecauseAVOoperatesatthelevelofvariation
operatorsratherthanbeingtiedtoaspecificdomain,itpointstowardabroaderpathforautonomous
optimization beyond attention kernels, including other performance-critical software systems on
diversehardwareplatforms,andengineeringorscientificdomainsthatdemandextendedautonomous
exploration.
Acknowledgement
WethanktheNVIDIACutlass,cuDNN,TensorRT-LLM,FlashInfer,DevTech,IPP,andCompiler
teams for valuable feedback and support. We also thank the FlashAttention-4 authors for open-
sourcingtheirimplementationandbenchmarkscripts,whichservedasabaselineandareferencefor
thiswork.
References
[1] MichaelO’Neill,LeonardoVanneschi,StevenGustafson,andWolfgangBanzhaf. Openissues
ingeneticprogramming. GeneticProgrammingandEvolvableMachines,11(3):339–363,2010.
[2] Joel Lehman, Jonathan Gordon, Shawn Jain, Kamal Ndousse, Cathy Yeh, and Kenneth O.
Stanley. Evolution through large models. 2022. URL https://arxiv.org/abs/2206.
08896.
[3] BernardinoRomera-Paredes,MohammadaminBarekatain,AlexanderNovikov,MatejBalog,
M.PawanKumar,EmilienDupont,FranciscoJ.R.Ruiz,JordanS.Ellenberg,PengmingWang,
OmarFawzi,PushmeetKohli,andAlhusseinFawzi. Mathematicaldiscoveriesfromprogram
searchwithlargelanguagemodels. Nature,625:468–475,2024.
[4] AlexanderNovikov,NgânVu˜,MarvinEisenberger,EmilienDupont,Po-SenHuang,AdamZsolt
Wagner, Sergey Shirobokov, Borislav Kozlovskii, Francisco J. R. Ruiz, Abbas Mehrabian,
10

M.PawanKumar,AbigailSee,SwaratChaudhuri,GeorgeHolland,AlexDavies,Sebastian
Nowozin,PushmeetKohli,andMatejBalog. Alphaevolve: Acodingagentforscientificand
algorithmicdiscovery,2025. URLhttps://arxiv.org/abs/2506.13131.
[5] Angelica Chen, David M. Dohan, and David R. So. Evoprompting: Language models for
code-levelneuralarchitecturesearch. 2023. URLhttps://arxiv.org/abs/2302.14838.
[6] AshishVaswani,NoamShazeer,NikiParmar,JakobUszkoreit,LlionJones,AidanN.Gomez,
LukaszKaiser,andIlliaPolosukhin. Attentionisallyouneed. 2023. URLhttps://arxiv.
org/abs/1706.03762.
[7] TriDao,DanielY.Fu,StefanoErmon,AtriRudra,andChristopherRé. Flashattention: Fast
andmemory-efficientexactattentionwithio-awareness. 2022. URLhttps://arxiv.org/
abs/2205.14135.
[8] TriDao. Flashattention-2: Fasterattentionwithbetterparallelismandworkpartitioning. 2023.
URLhttps://arxiv.org/abs/2307.08691.
[9] Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, and Tri Dao.
Flashattention-3: Fastandaccurateattentionwithasynchronyandlow-precision. 2024. URL
https://arxiv.org/abs/2407.08608.
[10] Ted Zadouri, Markus Hoehnerbach, Jay Shah, Timmy Liu, Vijay Thakkar, and Tri Dao.
Flashattention-4: Algorithmandkernelpipeliningco-designforasymmetrichardwarescaling.
2026. URLhttps://arxiv.org/abs/2603.05451.
[11] Sharan Chetlur, Cliff Woolley, Philippe Vandermersch, Jonathan Cohen, John Tran, Bryan
Catanzaro,andEvanShelhamer. cudnn: Efficientprimitivesfordeeplearning. 2014. URL
https://arxiv.org/abs/1410.0759.
[12] Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and
KarthikNarasimhan. Swe-bench: Canlanguagemodelsresolvereal-worldgithubissues? 2024.
URLhttps://arxiv.org/abs/2310.06770.
[13] John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik
Narasimhan,andOfirPress. Swe-agent: Agent-computerinterfacesenableautomatedsoftware
engineering. 2024. URLhttps://arxiv.org/abs/2405.15793.
[14] XingyaoWang,BoxuanLi,YufanSong,FrankF.Xu,XiangruTang,MingchenZhuge,JiayiPan,
YueqiSong,BowenLi,JaskiratSingh,HoangH.Tran,FuqiangLi,RenMa,MingzhangZheng,
BillQian,YanjunShao,NiklasMuennighoff,YizheZhang,BinyuanHui,JunyangLin,Robert
Brennan,HaoPeng,HengJi,andGrahamNeubig.Openhands:Anopenplatformforaisoftware
developersasgeneralistagents. 2025. URLhttps://arxiv.org/abs/2407.16741.
[15] Anthropic. Claude 3.7 sonnet and claude code. https://www.anthropic.com/news/
claude-3-7-sonnet,February2025. Accessed: 2026-03-25.
[16] OpenAI. https://openai.com/index/introducing-codex/. https://openai.com/index/
introducing-codex/,May2025. Accessed: 2026-03-25.
[17] Bing Xu, Terry Chen, Fengzhe Zhou, Tianqi Chen, Yangqing Jia, Vinod Grover, Haicheng
Wu,WeiLiu,CraigWittenbrink,WenmeiHwu,RogerBringmann,Ming-YuLiu,LuisCeze,
Michael Lightstone, and Humphrey Shi. VibeTensor: System Software for Deep Learning,
FullyGeneratedbyAIAgents. 2026.
[18] ChunhuiWan,XunanDai,ZhuoWang,MingleiLi,YanpengWang,YinanMao,YuLan,and
ZhiwenXiao. Loongflow: Directedevolutionarysearchviaacognitiveplan-execute-summarize
paradigm. 2025. URLhttps://arxiv.org/abs/2512.24077.
[19] ThomasBäck,DavidBFogel,andZbigniewMichalewicz. Handbookofevolutionarycomputa-
tion. Release,97(1):B1,1997.
[20] HaoranYe,JiaruiWang,ZhiguangCao,FedericoBerto,ChuanboHua,HaeyeonKim,Jinkyoo
Park, and Guojie Song. Reevo: Large language models as hyper-heuristics with reflective
evolution. 2024. URLhttps://arxiv.org/abs/2402.01145.
11

[21] Jean-BaptisteMouretandJeffClune. Illuminatingsearchspacesbymappingelites. 2015.
[22] MertYuksekgonul,DanielKoceja,XinhaoLi,FedericoBianchi,JedMcCaleb,XiaolongWang,
JanKautz,YejinChoi,JamesZou,CarlosGuestrin,andYuSun. Learningtodiscoverattest
|     | time. 2026. | URLhttps://arxiv.org/abs/2601.16175. |     |     |     |     |     |     |     |
| --- | ----------- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
[23] DavidSilver,AjaHuang,ChrisJMaddison,ArthurGuez,LaurentSifre,GeorgeVanDenDriess-
che,JulianSchrittwieser,IoannisAntonoglou,VedaPanneershelvam,MarcLanctot,etal. Mas-
teringthegameofgowithdeepneuralnetworksandtreesearch. nature,529(7587):484–489,
2016.
[24] AnYang,AnfengLi,BaosongYang,BeichenZhang,BinyuanHui,BoZheng,BowenYu,Chang
Gao,ChengenHuang,ChenxuLv,ChujieZheng,DayihengLiu,FanZhou,FeiHuang,FengHu,
HaoGe,HaoranWei,HuanLin,JialongTang,JianYang,JianhongTu,JianweiZhang,Jianxin
Yang,JiaxiYang,JingZhou,JingrenZhou,JunyangLin,KaiDang,KeqinBao,KexinYang,
LeYu,LianghaoDeng,MeiLi,MingfengXue,MingzeLi,PeiZhang,PengWang,QinZhu,Rui
Men,RuizeGao,ShixuanLiu,ShuangLuo,TianhaoLi,TianyiTang,WenbiaoYin,Xingzhang
Ren,XinyuWang,XinyuZhang,XuanchengRen,YangFan,YangSu,YichangZhang,Yinger
Zhang,YuWan,YuqiongLiu,ZekunWang,ZeyuCui,ZhenruZhang,ZhipengZhou,andZihan
Qiu. Qwen3technicalreport. 2025. URLhttps://arxiv.org/abs/2505.09388.
A ComparisonUsingFA4-ReportedBaselinePerformance
Section4reportscuDNNandFA4throughputmeasuredonourhardware. Inpractice,minorsystem-
leveldifferences(driverversions,thermalconditions,clockfrequencies)canaffectabsoluteTFLOPS.
Therefore,weadditionallycompareAVOagainstthecuDNNandFA4numberspublishedintheFA4
| paper[10]. | Figure7presentsthiscomparison.        |     |      |      |      |                                      |     |     |     |
| ---------- | ------------------------------------- | --- | ---- | ---- | ---- | ------------------------------------ | --- | --- | --- |
|            | Forward TFLOPS on B200 (causal=False) |     |      |      |      | Forward TFLOPS on B200 (causal=True) |     |     |     |
| 1800       | cuDNN                                 |     |      |      | 1800 | cuDNN                                |     |     |     |
|            | FA4                                   |     |      |      |      | FA4                                  |     |     |     |
| 1700       | AVO                                   |     | 1664 | 1668 | 1700 | AVO                                  |     |     |     |
1637
|      |               | 15851579 1615 | 16091601 | 16131613 |      |     |     | 1582 |      |
| ---- | ------------- | ------------- | -------- | -------- | ---- | --- | --- | ---- | ---- |
| 1600 | 15521532 1573 |               |          |          | 1600 |     |     |      | 1576 |
15091526 1540
| 1500   |     |     |     |     | 1500   |     | 1482     |     |     |
| ------ | --- | --- | --- | --- | ------ | --- | -------- | --- | --- |
| SPOLFT |     |     |     |     | SPOLFT |     | 14301426 |     |     |
1392
| 1400 |        |        |        |        | 1400 |          |        |        |        |
| ---- | ------ | ------ | ------ | ------ | ---- | -------- | ------ | ------ | ------ |
| 1300 |        |        |        |        | 1300 | 12951279 |        |        |        |
| 1200 |        |        |        |        | 1200 |          |        |        |        |
| 1100 |        |        |        |        | 1100 |          |        |        |        |
| 1000 | 4K     | 8K     | 16K    | 32K    | 1000 | 4K       | 8K     | 16K    | 32K    |
|      | (bs=8) | (bs=4) | (bs=2) | (bs=1) |      | (bs=8)   | (bs=4) | (bs=2) | (bs=1) |
Figure7: Multi-headattentionforward-passthroughput(TFLOPS)onNVIDIAB200,comparing
AVO(measuredonourhardware)againstcuDNNandFA4baselinenumbersasreportedintheFA4
| paper[10]. | Headdimension128,16heads,BF16. |     |     |     | Left: | non-causal. | Right: | causal. |     |
| ---------- | ------------------------------ | --- | --- | --- | ----- | ----------- | ------ | ------- | --- |
On non-causal attention, AVO outperforms the FA4-reported baselines across all configurations,
withgainsof+1.4%to+3.4%overcuDNNand+2.3%to+3.9%overFA4. Oncausalattention,
AVO achieves +3.6% to +7.5% over cuDNN and +3.7% to +8.8% over FA4, with the largest
gainsobservedatshortersequences(bs=8,seq=4096). Theseresultsarebroadlyconsistentwiththe
comparisonsinSection4.
12